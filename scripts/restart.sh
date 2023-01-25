#!/bin/bash
kill $(cat pid)
sleep 2
sh /mnt/thumb/waffle/scripts/start.sh