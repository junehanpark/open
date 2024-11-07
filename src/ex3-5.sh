#!/bin/sh

checkfile()
{
	echo "Inside the function"
	ls $1
}

echo "starting program"
checkfile $1
echo "closing program"

exit 0
