#!/bin/bash

if [ -d "$1"]; then
	echo
else
	mkdir $1
	cd "$1" || exit
	
	i=0
	while [ $i -lt 5 ]; do
		touch "file$i.txt"
		i=$((i + 1))
	done
	
	tar cvf "$1.tar" file0.txt file2.txt file3.txt file4.txt
	
	mv "$1.tar" .
	
	tar xvf "$1.tar"
	
fi
exit 0
