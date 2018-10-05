#/bin/bash

#This is to run on the VM itself in order to access the docker container
#and backup the Logs


#Path to data backups
backup_path="/home/daniel/miele/logs"
date=$(date +%F)

# Set default file permissions
umask 177

# Dump logs into log file
docker exec miele_prod sh -c "cat logs/MIE02-${date}.log" > $backup_path/MIE02-$date.log

chown daniel $backup_path/MIE02-$date.log
# TODO: Remove files older than 30 days