
netstat -c --numeric-hosts | grep tcp | grep ESTABLISHED | xargs -n6 | awk '{print $5}'

