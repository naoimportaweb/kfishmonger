#!/bin/bash

cd /opt/kfishmonger/command/

background=0
for i; do 
   if [ $i = "-b" ] ; then
      background=1
   fi 
done

if [ $background -eq 1 ] ; then
    python3 kfm.py $@ &
else
    python3 kfm.py $@
fi