#!/bin/sh

if [ "$1" == "--create" ] ; then
	NAME="$2"
	VNAME="vroot_$2"
	IMAGE=$3

	if [ "x$IMAGE" == "x" ] ; then
		IMAGE="ubuntu:latest"
	fi

	sudo docker create -it --name $VNAME -u $USER -w $HOME --net=host \
		-e VROOT_NAME="$NAME" \
		-v /home:/home \
		-v /etc/passwd:/etc/passwd:ro \
		-v /etc/group:/etc/group:ro \
		-v /etc/sudoers:/etc/sudoers:ro \
		-v /etc/shadow:/etc/shadow:ro \
		$IMAGE \
		/bin/bash
elif [ "$1" == "--list" ] ; then
	sudo docker ps -a  | grep "vroot\|CONTAINER ID"
elif [ "$1" == "--rm" ] ; then
	NAME="vroot_$2"
	sudo docker rm $NAME
else
	NAME="vroot_$1"
	running=`sudo docker inspect $NAME | grep "Running" | awk '{print $2}'`
	if [ "$running" == "false," ] ; then
		sudo docker start -ai $NAME
	else
		sudo docker attach $NAME
	fi
	#sudo docker attach $NAME
fi
