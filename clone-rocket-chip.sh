#!/bin/bash

TOP=$PWD/rocket-chip
CLONE=$PWD/clone

function get_submodules {
    cd $1
    cp $2 .gitmodules
    git submodule update --init
    git checkout .gitmodules
}

function get_riscv_tools {
    cd $1
    cp $2 .gitmodules
    git submodule update --init --recursive
    git checkout .gitmodules
}


git clone https://git.oschina.net/cnrv/rocket-chip $TOP

get_submodules   $TOP                           $CLONE/rocket-chip.gitmodules
get_riscv_tools  $TOP/riscv-tools               $CLONE/riscv-tools.gitmodules
get_submodules   $TOP/riscv-tools/riscv-tests   $CLONE/riscv-tests.gitmodules
get_submodules   $TOP/riscv-tools/riscv-llvm    $CLONE/riscv-llvm.gitmodules

cd $TOP
git submodule update --init --recursive


