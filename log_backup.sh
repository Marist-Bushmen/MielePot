#!/bin/bash

#This is to run on the VM itself in order to access the docker container
#and backup the Logs


#Path to data backups
backup_path="/home/dgisolfi/projects/miele/logs/"
filename="MIE02-$(date +%F).log"

# Set default file permissions
umask 177

# Dump logs into log file
docker exec miele_prod sh -c 'cat MIE02.log' > $backup_path/$filename
#TODO: Remove files older than 30 days
