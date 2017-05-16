import sys

GITHUB_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

USERNAME="????"
PASSWORD="????"

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

def create_projects(org_repos):
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support.ui import Select 
	from selenium.webdriver.support import expected_conditions as EC
	from pprint import pprint
	import time
	
	driver = webdriver.Firefox()
	driver.get("https://git.oschina.net/login")
	
	driver.find_element_by_id("user_login").send_keys(USERNAME)
	driver.find_element_by_id("user_password").send_keys(PASSWORD)
	driver.find_element_by_id("new_user").submit()
	
	try:
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "followers-number"))
		)
	except Exception, e:
		print "Failed at login", e
		sys.exit(-1)

	for org_repo in org_repos:
		org, repo = org_repo
		print "Start Create Project: %s/%s on git.oschina.net" % (org, repo)
		try:
			driver.get("https://git.oschina.net/projects/new")
			element = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.ID, "git-footer-main"))
			)
		except Exception, e:
			print "Failed at repo: %s [%s]" % (org_repo, e)
			sys.exit(-1)

			
		driver.find_element_by_xpath('//div[text()="cnrv-riscv"]').click()
		driver.find_element_by_xpath('//div[text()="cnrv-%s"]' % org).click()
		
	#	driver.find_element_by_id("import-link").click()
	#	driver.find_element_by_id("project_import_url").clear()
	#	driver.find_element_by_id("project_import_url").send_keys("https://github.com/%s/%s" % (org, repo))

		driver.find_element_by_id("project_name").clear()
		driver.find_element_by_id("project_name").send_keys(repo)
		
		driver.find_element_by_id("readme").click()
		
		
		driver.find_element_by_id("new_project").submit()
		print "Wait 3s"
		time.sleep(3)

def main():
	org_repos = get_org_repos()
	create_projects(org_repos)

if __name__ == "__main__":
	main()
