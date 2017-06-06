GITHUB_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def get_org_repos():
	from github import Github
	g = Github(GITHUB_KEY)

	orgs_list = ['riscv', 'ucb-bar', 'sifive', 'lowrisc']

	org_repos = []
	for org in orgs_list:
		print "Fetching repos for %s" % org
		for repo in g.get_user(org).get_repos():
			print "\tGet repo: %s" % repo.full_name
			org_repos.append( (org, repo.name) )

	return org_repos
def main():
	org_repos = get_org_repos()
	for org_repo in org_repos:
		org, repo = org_repo
		print "  - PRJ=%-40s       SRC=https://github.com/%s" % (repo, org)
		

if __name__ == "__main__":
	
	main()
