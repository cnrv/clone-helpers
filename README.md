如何利用国内镜像下载RISC-V工程
==================

为了方便国内的RISC-V爱好者下载GitHub上的RISC-V工程，我们在`http://git.oschina.net`上镜像了主要的RISC-V工程。
我们利用国外服务器定期同步oschina上的镜像，方便大家获得最新的更新。

### 下载Rocket-Chip工程

~~~
git clone https://github.com/cnrv/clone-helpers.git
cd clone-helpers
./clone-rocket-chip.sh
~~~

Rocket-Chip被下载到`clone-helper/rocket-chip`。
所有的submodule地址都被重定向到`http://git.oschina.net`并可以通过`git submodule update --recursive`获得最新的代码。

*注意事项*：submodule的远程地址被内部重定向到`http://git.oschina.net`而不受`.gitmodules控制。
如果需要更改.gitmodule，整个工程可能需要重新下载。具体原因请参看下面的镜像机理部分的说明。

镜像的机理
======================

所有的RISC-V工程被定期自动的同步到oschina的服务器。
为了能在修改工程代码的情况下重定向子模块远程地址，我们利用了git的内部机制：

以rocket-chip的子模块chisel3为例，当chisel3子模块被`git submodule --init`命令初始化后，其远程地址被拷贝到`.git/modules/chisel3/config`。
此后，修改`chisel3/.gitmodules`并不会自动改变chisel3模块的远程地址。
`git submodule update`命令仍然会使用`.git/modules/chisel3/config`定义的远程地址。

利用该特性，`clone-rocket-chip.sh`在初始化子模块时，会先用clone文件夹下的submodule文件替代`.gitmodule`，然后初始化子模块。
这样，子模块的远程地址就被重定向。当子模块初始完成后，`.gitmodules`文件就被恢复，所以工程代码并没有被改变。


帮助我们同步镜像
=======================
我们需要在国外的RISC-V爱好者帮助我们同步镜像到oschina。
如果你有一台经常开机的电脑，有较快的网络速度，链接GitHub和oschina的速度都比较快，那么，我们需要你！ :-)

### 设定同步服务器

1. 联系cnrv的管理员，获得oschina里镜像工程的读写权。
2. 生成电脑的ssh公钥，并添加到自己的oschina SSH keys (http://git.oschina.net/profile/sshkeys)
3. 建立一个同步缓冲文件夹，比如 `mkdir -p /mnt/scrtach/cnrv-sync`
4. 将sync.sh添加到电脑的cron计划中，比如在`/etc/crontab`中添加<br>
`00 * * * *   USERID   WORK=/mnt/scrtach/cnrv-sync PATH-TO-THIS-REPO/sync.sh`<br>
`USERID`是你的用户名，`PATH-TO-THIS-REPO`是该repo的本地地址。
*注意*：第一次会下载和上传接近几个GB的数据，根据你的网速，也许要半小时到一小时。


