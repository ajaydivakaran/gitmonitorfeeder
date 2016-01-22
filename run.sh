#!/bin/sh

function usage
{
	echo "To post to elastic search , usage: ./run.sh -post"	
}

if [ "$1" == "" ]; then
	usage
	exit 1
fi

if [ "$1" == "-post" ]; then
	echo "Posting to elastic search"
fi

function run
{
	python repo_scan/app.py $1
}

run
