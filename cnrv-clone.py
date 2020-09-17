#!/usr/bin/python2

import argparse
import os
import subprocess
import stdconfigparser

################### help functions ###############

# trim ending ".git"
def trim_git(url):
    l = len(url)
    if (l > 4 and url[l-4:] == '.git'):
        return url[:l-4]
    else:
        return url    

# replace lowrisc with lowRISC
def fix_url(url):
    return trim_git(url).replace('/lowrisc/', '/lowRISC/')

def url_to_tuple(url, parent=None):
    t = fix_url(url).split('/')
    if(parent != None and t[0] == ".."):
        return (parent[0], parent[1], parent[2], t[1])
    else:
        return (t[0], t[2], t[3], t[4])

def tuple_to_url(url):
    return "" + url[0] + "//" + url[1] + "/" + url[2] + "/" + url[3]

def remote_exist(url):
    return subprocess.call("git ls-remote " + tuple_to_url(url) + ' > /dev/null', shell=True)

def get_cnrv_image(url):
    print("===> check for potential CNRV image. (ignore errors below)")
    cnrv = ("https:", "git.oschina.net", "cnrv-"+url[2], url[3])
    if (0 != remote_exist(cnrv)):
        print("INFO: There is no image available from CNRV for repository " + tuple_to_url(url) + ", use the original instead.")
        cnrv = url
    else:
        print("INFO: Find an available CNRV image at " + tuple_to_url(cnrv))
    print("<===")
    return cnrv

def update_submodule_config(cfg_parser):
    sm_cfg_file = open(".gitmodules", 'w')
    cfg_parser.write(sm_cfg_file)
    sm_cfg_file.close()

def fix_head_branch():
    print("===> fix the ambiguous HEAD branch issue. (ignore errors below)")
    head_commit =  subprocess.check_output('git show --pretty=tformat:%H | head -n 1', shell=True)
    if 0 == subprocess.call("git branch -m HEAD cnrv_fix_head", shell=True):
        subprocess.call("git checkout " + head_commit, shell=True)
        subprocess.call("git branch -D cnrv_fix_head", shell=True)
    print("<===")

# the recursive submodule checkout function
def proc_submodules(remote):
    # check whether there are submodules
    if not os.path.isfile(".gitmodules"):
        return

    # read the submodule configuration
    sm_cfg = stdconfigparser.StdConfigParser()
    sm_cfg.read(".gitmodules")
    cur_dir = os.getcwd()
    for sm in sm_cfg.sections():
        sm_path = sm_cfg.get(sm, "path")
        print("\n==============================")
        print("Process submodule " + sm_path)
        orig_url = url_to_tuple(sm_cfg.get(sm, "url"), remote)
        cnrv_url = get_cnrv_image(orig_url)

        sm_cfg.set(sm, "url", tuple_to_url(cnrv_url))
        update_submodule_config(sm_cfg)
        rv = subprocess.call("git submodule update --init " + sm_path, shell=True)
        sm_cfg.set(sm, "url", tuple_to_url(orig_url))
        update_submodule_config(sm_cfg)
        subprocess.call("git submodule sync " + sm_path, shell=True)
        subprocess.call("git submodule update --init " + sm_path, shell=True)
        # recursively checkout the submodule
        os.chdir(sm_path)
        fix_head_branch()
        proc_submodules(orig_url)
        os.chdir(cur_dir)
    subprocess.call("git checkout .gitmodules", shell=True)

################### actual script ################

# analyse the argument list
parser = argparse.ArgumentParser(description='Smart clone a repo from available CNRV images.')
parser.add_argument('repo', metavar='repository', nargs=1,
                    help='URL of the remote repository to clone')
parser.add_argument('dir', metavar='directory', nargs='?',
                    help='Directory of the local clone.')
parser.add_argument('-b', dest='branch',
                    help='The branch to be cloned (default: master / auto-detect)')
parser.add_argument('--recursive', action='store_true', dest='recursive',
                    help='Checkout all submodules recursively.')
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
    remote_refs = subprocess.check_output("git ls-remote " + tuple_to_url(remote), shell=True)
    head_commit = ""
    master_commit = ""
    commit_dic = {}
    for line in remote_refs.split('\n'):
        if line != "":
            record = line.split()
            if record[1] == "HEAD":
                head_commit = record[0]
            elif record[1] == "refs/heads/master":
                master_commit = record[0]
            else:
                commit_dic[record[0]] = record[1]

    if master_commit != "":
        master_branch = "master"
    else:
        master_branch = commit_dic[head_commit].split('/')[-1]

# bookkeeping
root_dir = os.getcwd()

######################## clone the repo ###########################

# clone the project
subprocess.check_call("git clone -b " + master_branch + " " + tuple_to_url(cnrv_remote) + " " + work_dir, shell=True)

# enter the project
os.chdir(work_dir)

# recover the original remote url
subprocess.check_call("git remote set-url origin " + tuple_to_url(remote), shell=True)

# fix the potential HEAD branch
fix_head_branch()

if args.recursive :
    # recursively process all submodules
    proc_submodules(remote)

    # do a final submodules checout recursively
    subprocess.call("git submodule update --init --recursive", shell=True)

######################## End of script ############################
os.chdir(root_dir)

