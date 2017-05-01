#!/bin/bash

# usage:  WORK=/PATH/TO/WORK/DIR sync.sh

function sync_repo {
    PROJ="$1"
    ORIG_URL="$2"
    CNRV_URL="$3"

    echo "------------------------------------------------------------------------------"
    echo "Sync Project: $PROJ"
    echo "  From: $ORIG_URL/$PROJ"
    echo "  To:   $CNRV_URL/$PROJ"
    echo

    if [ ! -e $WORK/$PROJ ]; then
        git clone --verbose $ORIG_URL/$PROJ $WORK/$PROJ
    fi

    cd $WORK/$PROJ
    git fetch --verbose

    # simple retry 3 times.
    git push --verbose $CNRV_URL/$PROJ +refs/remotes/origin/*:refs/heads/* +refs/tags/*:refs/tags/*
}

if [ "x$WORK" = "x" ]; then
    echo "WORK is not defined."
else
    sync_repo  $PRJ $SRC $DST
fi
