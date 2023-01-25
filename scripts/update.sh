#!/bin/bash
kill $(cat /mnt/thumb/waffle/scripts/pid)
sleep 2
git pull origin master
sleep 5
sh /mnt/thumb/waffle/scripts/start.sh
