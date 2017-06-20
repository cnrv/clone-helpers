如何利用国内镜像下载RISC-V工程
==================

为了方便国内的RISC-V爱好者下载GitHub上的RISC-V工程，我们在`http://git.oschina.net`上镜像了主要的RISC-V工程。
我们利用国外服务器定期同步oschina上的镜像，方便大家获得最新的更新。

### 下载Rocket-Chip工程

~~~shell
git clone https://github.com/cnrv/clone-helpers.git
cd clone-helpers
./cnrv-clone.py --recursive https://github.com/ucb-bar/rocket-chip.git
~~~

用于下载的`cnrv-clone.py`脚本需要用到3个python程序包:
* stdconfigparser<br>
  解析git工程的submodule配置
* argparse<br>
  解析脚本输入参数
* subprocess<br>
  在python环境中执行系统命令

其中argparse和subprocess应该被python 2.7默认安装。stdconfigparser需要单独安装：

~~~shell
sudo apt-get install python-pip
sudo pip install stdconfigparser
~~~

### 下载其他工程

该下载脚本也可用于下载其他的RISC-V工程。根据工程的地址，脚本会自动检索工程是否被oschina镜像。如果有镜像，则会选择从镜像下载，否则从源地址下载。
脚本的具体参数如下：

~~~shell
$ ./cnrv-clone.py -h
usage: cnrv-clone.py [-h] [-b BRANCH] [--recursive] repository [directory]

Smart clone a repo from available CNRV images.

positional arguments:
  repository   URL of the remote repository to clone
  directory    Directory of the local clone.

optional arguments:
  -h, --help   show this help message and exit
  -b BRANCH    The branch to be cloned (default: master / auto-detect)
  --recursive  Checkout all submodules recursively.
~~~

### 现在已被镜像的工程

具体的工程列表可参看`.travis.yml`文件。其中几个被经常下载的工程包括：

* https://github.com/riscv/riscv-linux
* https://github.com/riscv/riscv-tools
* https://github.com/ucb-bar/rocket-chip
* https://github.com/ucb-bar/chisel
* https://github.com/sifive/freedom
* https://github.com/sifive/freedom-e-sdk
* https://github.com/sifive/freedom-u-sdk
* https://github.com/lowrisc/lowrisc-chip



