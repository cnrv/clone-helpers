from git import Repo

INC_STEP = 1000

repo = Repo(".")
with open("push.sh", 'w') as f:
	for ref in repo.refs:
		if ref.name.startswith("origin/") and ref.name != "origin/HEAD":
			f.write("echo %s\n" % ("-" * 80))
			f.write("echo push branch: %s\n" % ref.name)

			cnrv_branch_exist = len(filter(lambda r: r.name == ("cnrv/%s" % ref.name), repo.refs)) > 0

			# check the remote status
			if cnrv_branch_exist is True:
				commits = repo.git.rev_list("cnrv/%s..%s" % (ref.name, ref.name)).splitlines()
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
					f.write("echo git push -v %s %s:refs/heads/%s\n" % ('cnrv', push_commit, ref.name))
					f.write("git push -v %s %s:refs/heads/%s\n" % ('cnrv', push_commit, ref.name))
