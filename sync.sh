#!/bin/bash

# usage:  WORK=/PATH/TO/WORK/DIR sync.sh

function sync_repo {
    PROJ="$1"
    ORIG_URL="$2"
    CNRV_URL="$3"

    if [ ! -e $WORK/$PROJ ]; then
        git clone $ORIG_URL/$PROJ $WORK/$PROJ
    fi

    cd $WORK/$PROJ
    git fetch
    git push --mirror $CNRV_URL/$PROJ
    git push $CNRV_URL/$PROJ +refs/remotes/origin/*:refs/heads/* +refs/tags/*:refs/tags/*
    cd -
}

if [ "x$WORK" = "x" ]; then
    echo "WORK is not defined."
else
    sync_repo   riscv-test-env       https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-tests          https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-pk             https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-opcodes        https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-llvm           https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-clang          https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-isa-sim        https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-newlib         https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-dejagnu        https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-glibc          https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-gcc            https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-binutils-gdb   https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-gnu-toolchain  https://github.com/riscv   git@git.oschina.net:cnrv
    sync_repo   riscv-fesvr          https://github.com/riscv   git@git.oschina.net:cnrv

    sync_repo   riscv-torture        https://github.com/ucb-bar git@git.oschina.net:cnrv
    sync_repo   berkeley-hardfloat   https://github.com/ucb-bar git@git.oschina.net:cnrv
    sync_repo   firrtl               https://github.com/ucb-bar git@git.oschina.net:cnrv
    sync_repo   chisel3              https://github.com/ucb-bar git@git.oschina.net:cnrv
    sync_repo   rocket-chip          https://github.com/ucb-bar git@git.oschina.net:cnrv
fi
