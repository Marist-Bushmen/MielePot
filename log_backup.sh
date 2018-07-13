#!/bin/bash

#This is to run on the VM itself in order to access the docker container
#and backup the Logs


#Path to data backups
backup_path="/home/dgisolfi/projects/miele/logs/"
date=$(date +"%d-%b-%Y")

# Set default file permissions
umask 177

# Dump logs into log file
docker exec miele_prod sh -c 'cat Miele.log' >> $backup_path/ Log-$date.log

#TODO: Remove files older than 30 days
