#!/bin/bash

TOP=$PWD/rocket-chip
CLONE=$PWD/clone

function get_submodules {
    cd $1
    cp $2 .gitmodules
    git submodule update --init
    git checkout .gitmodules
}


git clone https://git.oschina.net/cnrv/rocket-chip $TOP

# rocket-chip
get_submodules  $TOP   $CLONE/rocket-chip.gitmodules


