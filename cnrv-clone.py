import argparse
import os
import subprocess

################### help functions ###############

# trim ending ".git"
def trim_git(url):
    l = len(url)
    if (url[l-4:] == '.git'):
        return url[:l-4]
    else:
        return url    

# replace lowrisc with lowRISC
def fix_url(url):
    return url.replace('/lowrisc/', '/lowRISC/')

def url_to_tuple(url):
    t = url.split('/')
    return (t[0], t[2], t[3], t[4])

def tuple_to_url(url):
    return "" + url[0] + "//" + url[1] + "/" + url[2] + "/" + url[3]

def remote_exist(url):
    return subprocess.call("git ls-remote " + tuple_to_url(url) + ' > /dev/null')


################### actual script ################

# analyse the argument list
parser = argparse.ArgumentParser(description='Smart clone a repo from available CNRV images.')
parser.add_argument('repo', metavar='repository', nargs=1,
                    help='URL of the remote repository to clone')
parser.add_argument('dir', metavar='directory', nargs='?',
                    help='Directory of the local clone.')
parser.add_argument('-b', dest='branch',
                    help='sum the integers (default: find the max)')
args = parser.parse_args()

# analyse the remote repo URL
remote = url_to_tuple(trim_git(fix_url(args.repo[0])))
if 0 != remote_exist(remote):
    print("ERROR: remote repository " + tuple_to_url(remote) + " does not exist!")
    exit(1)

# check the available clone from CNRV
cnrv_remote = ("https:", "git.oschina.net", "cnrv-"+remote[2], remote[3])
if (0 != remote_exist(cnrv_remote)):
    print("INFO: There is no image available from CNRV for repository " + tuple_to_url(remote) + ", use the original instead.")
    cnrv_remote = remote

# analyse the local repo directory
work_dir = args.dir
if work_dir is None:
    work_dir = remote[3]

if os.path.exists(work_dir):
    print("ERROR: the local clone directory " + work_dir + " already exists!")
    exit(1)

# analyse the branch name
master_branch = args.branch
if master_branch is None:
    master_branch = subprocess.check_output("git ls-remote --symref " + tuple_to_url(remote) + " HEAD")
    master_branch = master_branch.split()[1].split('/')[2]

print(remote)
print(cnrv_remote)
print(work_dir)
print(master_branch)
