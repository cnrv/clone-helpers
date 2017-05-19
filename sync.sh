#!/bin/bash

# usage:  WORK=/PATH/TO/WORK/DIR sync.sh

function sync_repo {
    PROJ="$1"
    SRC_ORIG="$2"
    CNRV_URL="$3"
    SCRIPT_DIR="$4"

    echo "------------------------------------------------------------------------------"
    echo "Sync Project: $PROJ"
    echo "  From: $SRC_ORIG/$PROJ"
    echo "  To:   CNRV-MIRROR/$PROJ"
    echo

    if [ ! -e $WORK/$SRC_ORIG/$PROJ ]; then
        git clone --verbose https://github.com/$SRC_ORIG/$PROJ $WORK/$SRC_ORIG/$PROJ
    fi

    cd $WORK/$SRC_ORIG/$PROJ
    git fetch -v origin --verbose

    git remote -v add cnrv $CNRV_URL/cnrv-$SRC_ORIG/$PROJ || true

    git fetch -v cnrv --verbose

    python $SCRIPT_DIR/push.py

    source push.sh

    echo "PUSH to cnrv"
    git push -v cnrv +refs/remotes/origin/*:refs/heads/* +refs/tags/*:refs/tags/*
}

if [ "x$WORK" = "x" ]; then
    echo "WORK is not defined."
else
    sync_repo  $PRJ $SRC_ORIG $DST_ENC_URL $TRAVIS_BUILD_DIR
fi
