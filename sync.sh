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

    if [ ! -e $WORK/$PROJ ]; then
        git clone --verbose https://github.com/$SRC_ORIG/$PROJ $WORK/$PROJ
    fi

    cd $WORK/$PROJ
    git fetch --verbose

    echo "PUSH to cnrv"
    git push -q $CNRV_URL/cnrv-$SRC_ORIG/$PROJ +refs/remotes/origin/*:refs/heads/* +refs/tags/*:refs/tags/*
}

if [ "x$WORK" = "x" ]; then
    echo "WORK is not defined."
else
    sync_repo  $PRJ $SRC $DST_ENC_URL
fi
