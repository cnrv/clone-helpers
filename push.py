from git import Repo

INC_STEP = 2000

repo = Repo(".")
cnrv_remote_ref_sets = set()

print "Cache all cnrv remote cache"
for ref in repo.refs:
	if ref.name.startswith("cnrv/") and ref.name != "cnrv/HEAD":
		print "\tprocessing... branch", ref.name
		commits = repo.git.rev_list(ref.name).splitlines()
		cnrv_remote_ref_sets |= set(commits)

print "Start generate push script"
with open("push.sh", 'w') as f:
	for ref in repo.refs:
		if ref.name.startswith("origin/") and ref.name != "origin/HEAD":
			print "\tprocessing... branch", ref.name
			f.write("echo %s\n" % ("-" * 80))
			f.write("echo push branch: %s\n" % ref.name)

			ref_wo_origin = ref.name[len('origin/'):]

			cnrv_branch_exist = len(filter(lambda r: r.name == ("cnrv/%s" % ref_wo_origin), repo.refs)) > 0

			# check the remote status
			if cnrv_branch_exist is True:
				commits = repo.git.rev_list("cnrv/%s..origin/%s" % (ref_wo_origin, ref_wo_origin)).splitlines()
			else:
				commits = repo.git.rev_list(ref.name).splitlines()

			clen = len(commits)
			if clen > 0:
				push_commits = []
				for i in range(0, clen, INC_STEP):
					push_commits.append(commits[i])
				push_commits.append(commits[-1])
				push_commits.reverse()
				for push_commit in push_commits:
					if push_commit in cnrv_remote_ref_sets and push_commit != push_commits[-1]:
						continue
					f.write("git push -v %s %s:refs/heads/%s\n" % ('cnrv', push_commit, ref_wo_origin))

				cnrv_remote_ref_sets |= set(push_commits)
