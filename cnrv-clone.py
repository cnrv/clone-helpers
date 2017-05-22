import argparse
import os
import subprocess
import stdconfigparser

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
    return trim_git(url).replace('/lowrisc/', '/lowRISC/')

def url_to_tuple(url):
    t = fix_url(url).split('/')
    return (t[0], t[2], t[3], t[4])

def tuple_to_url(url):
    return "" + url[0] + "//" + url[1] + "/" + url[2] + "/" + url[3]

def remote_exist(url):
    return subprocess.call("git ls-remote " + tuple_to_url(url) + ' > /dev/null')

def get_cnrv_image(url):
    cnrv = ("https:", "git.oschina.net", "cnrv-"+url[2], url[3])
    if (0 != remote_exist(cnrv)):
        print("INFO: There is no image available from CNRV for repository " + tuple_to_url(url) + ", use the original instead.")
        cnrv = url
    return cnrv

def update_submodule_config(cfg_parser):
    sm_cfg_file = open(".gitmodules", 'w')
    cfg_parser.write(sm_cfg_file)
    sm_cfg_file.close()

# the recursive submodule checkout function
def proc_submodules():
    # check whether there are submodules
    if not os.path.isfile(".gitmodules"):
        return

    # read the submodule configuration
    sm_cfg = stdconfigparser.StdConfigParser()
    sm_cfg.read(".gitmodules")
    cur_dir = os.getcwd()
    for sm in sm_cfg.sections():
        orig_url = url_to_tuple(sm_cfg.get(sm, "url"))
        cnrv_url = get_cnrv_image(orig_url)
        sm_path = sm_cfg.get(sm, "path")
        sm_cfg.set(sm, "url", tuple_to_url(cnrv_url))
        update_submodule_config(sm_cfg)
        rv = subprocess.call("git submodule update --init " + sm_path)
        sm_cfg.set(sm, "url", tuple_to_url(orig_url))
        update_submodule_config(sm_cfg)
        subprocess.call("git submodule sync " + sm_path)
        if rv:
            # somehow failed to get the expect commit from cnrv image
            # do it again from the original
            subprocess.call("git submodule update --init " + sm_path)
        # recursively checkout the submodule
        os.chdir(sm_path)
        proc_submodules()
        os.chdir(cur_dir)
    subprocess.call("git checkout .gitmodules")

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
remote = url_to_tuple(args.repo[0])
if 0 != remote_exist(remote):
    print("ERROR: remote repository " + tuple_to_url(remote) + " does not exist!")
    exit(1)

# check the available clone from CNRV
cnrv_remote = get_cnrv_image(remote)

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


# bookkeeping
root_dir = os.getcwd()

######################## clone the repo ###########################

# clone the project
subprocess.check_call("git clone -b " + master_branch + " " + tuple_to_url(cnrv_remote) + " " + work_dir)

# enter the project
os.chdir(work_dir)

# recover the original remote url
subprocess.check_call("git remote set-url origin " + tuple_to_url(remote))

# recursively process all submodules
proc_submodules()

# do a final submodules checout recursively
subprocess.call("git submodule update --init --recursive")

######################## End of script ############################
os.chdir(root_dir)

