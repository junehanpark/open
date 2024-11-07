#!/bin/sh

echo "Is it fun to learn linux? (y/n)"

read answer

case $answer in 
	yes|Y|y|uh-huh)
		echo "y";;
	no|n|N|nah)
		echo "n";;
	*)
		echo "y or n pls"
		exit 1;;
esac

exit 0
