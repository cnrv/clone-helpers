#!/bin/bash

# usage:  WORK=/PATH/TO/WORK/DIR sync.sh

function sync_repo {
    PROJ="$1"
    SRC_ORIG="$2"
    CNRV_URL="$3"

    echo "------------------------------------------------------------------------------"
    echo "Sync Project: $PROJ"
    echo "  From: $SRC_ORIG/$PROJ"
    echo "  To:   CNRV-MIRROR/$PROJ"
    echo

    if [ ! -e $WORK/$SRC_ORIG/$PROJ ]; then
        git clone --verbose https://github.com/$SRC_ORIG/$PROJ $WORK/$SRC_ORIG/$PROJ
    fi

    cd $WORK/$SRC_ORIG/$PROJ
    git fetch --verbose

    python push.py

    source push.sh

    echo "PUSH to cnrv"
    git push -v $CNRV_URL/cnrv-$SRC_ORIG/$PROJ +refs/remotes/origin/*:refs/heads/* +refs/tags/*:refs/tags/*
}

if [ "x$WORK" = "x" ]; then
    echo "WORK is not defined."
else
    sync_repo  $PRJ $SRC_ORIG $DST_ENC_URL
fi
