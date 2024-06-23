ls -Art | tail -n 1
find ~/ -type f -printf "%T@ %p\n" | sort -n | cut -d' ' -f 2- | tail -n 10
