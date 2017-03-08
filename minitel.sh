#!/bin/bash

#if [ $(id -u) -eq 0 ]; then
    #read -p "Enter username : " username
    #egrep "^$username" /etc/passwd >/dev/null
    #if [ $? -eq 0 ]; then
	#echo "$username exists!"
	#exit 1
    #else
	#useradd -ou 0 -g 0 $username
	#passwd $username
	#echo "$username ALL=(ALL:ALL) ALL" >> /etc/sudoers
	#[ $? -eq 0 ] && echo "User has been added to system!" || echo "Failed to add a user!"
	python my_minitel/minitel.py
	read -p "Add commentary ? y for yes, else for no put [y/n] " askComment
	 NOW=$(date +"%Y-%m-%d:%H:%M:%S")
	if [ $askComment == "y" ]; then
	    read -p "Write your comment :" Commentary
	    echo "Adding log => this program has been use at" $NOW "By" $USER "commentary :" $Commentary >> log/syslog.txt
	    echo "Your commentary has been added to the syslog !"
	    cat log/syslog.txt
        else
	    echo "Adding log => this program has been use at" $NOW "By" $USER "no commentary" >> log/syslog.txt
	    echo "No commentary added to the syslog !"
	    cat log/syslog.txt
	fi
    #fi
#else
    #echo "Only root may add a user to the system"
    #exit 2
#fi
