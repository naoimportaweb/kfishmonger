#!/bin/bash

cd /opt/kfishmonger/command/

# o comando requer que seja root ou sudo, obrigatorio
if [ "$EUID" -ne 0 ]
  then echo "Por favor, execute como root ou sudo"
  exit
fi

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