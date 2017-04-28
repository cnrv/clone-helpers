#!/bin/bash

ssh-agent bash -c 'ssh-add id_rsa; ./sync.sh'
