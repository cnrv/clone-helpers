from git import Repo
import sys

repo = Repo(".")
with open("push.sh", 'w') as f:
	for ref in repo.refs:
		if ref.name.startswith("origin/"):
			f.write("-" * 80 + "\n")
			f.write("echo push branch: %s\n" % ref.name)
			commits = repo.git.rev_list(ref.name).splitlines()
			clen = len(commits)
			push_commits = []
			for i in range(0, clen, 1000):
				push_commits.append(commits[i])
			push_commits.append(commits[-1])
			push_commits.reverse()
			for push_commit in push_commits:
				f.write("echo git push -v %s %s:refs/heads/%s || true\n" % (sys.argv[1], push_commit, ref.name))
				f.write("git push -v %s %s:refs/heads/%s || true\n" % (sys.argv[1], push_commit, ref.name))
