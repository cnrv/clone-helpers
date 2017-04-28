#!/bin/bash

ssh-keyscan -t $TRAVIS_SSH_KEY_TYPES -H git.oschina.net 2>&1 | tee -a $HOME/.ssh/known_hosts
