#!/bin/sh

if [ -d "$1" ]
then
	:
else
	mkdir $1
	cd $1
	i=0
	while [ $i -lt 5 ]
	do
		mkdir files$i
		touch "file$i.txt"
		ln -s file$i.txt file$i/file$i.txt
		i=$((i+1))
	done
fi
exit 0
