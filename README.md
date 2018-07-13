# MielePot
A basic honeypot to gather data on attempted logins, to be expanded on for further data collection. Currently, the honeypot is running at [dgisolfi.xyz:4400](http://dgisolfi.xyz:4400/)

### Author
Daniel Gisolfi - All current work - dgisolfi

## Prerequisites

All requirements to run an instance of this project

- Digital Ocean or an equivalent service
- Bootstrap 4(not needed but used for login form)
- Docker
- Flask

## Docker Implementation

The honeypot takes advantage of a docker container and is run using the image pull from docker hub. The image for this honeypot can be found [here](https://hub.docker.com/r/dgisolfi/mielepot/). The Dockerfile found in the root directory of this repository is used to create the mielepot image. The Docker file does the following:
1. pull the latest version of Ubuntu from docker hub
2. install the following: python-pip, python-dev, build-essential
3. Create a directory in the image, and copy all of src into it
4. install all python requirements
5. define the entry-point and command to run on startup

## Miele Pot Setup

### Container setup

The following is a basic guide on how to deploy the Miele honeypot. Start by place the two shell scripts from the repository into your production environment. After ensuring Docker is installed on the machine and that the shell scripts are executable run the following in the directory containing the two scripts:
```bash
./deploy_miele.sh
```
This will do the following:
1. prompt the user to login to Docker
2. pull the latest version of the Docker image
3. run an instance of the image as a container on port 4400

To see the running container run the following in any directory
```bash
docker ps -a
```
You will see a list of running and any exited containers, our honeypot is the one named "miele_prod". At this point, you should be able to go to the IP address of the machine running this container and see the honeypot on port 4400. If running on a local machine visit [localhost](http://0.0.0.0:4400)

### Logging setup
As is the Docker container will log all get and post requests to the site. However with Docker containers unless volumes are used all data is glossed once the container is killed. At any point, while a container is running you may enter the bash for that particular container to do so run the following on the host machine
```bash
docker exec -it miele_prod bash
```

 In order to save the logs taken by the honeypot, a system must be set up to copy the file over to the host machine. This can be done in many ways however I chose to use a cronjob with a shell script. The second shell script that was initially placed on the host machine will be used to do this. In the script edit the variable that sets the path to where logs will be saved. in my case, I created a directory called logs at the level of the shell scripts. when running the shell script will create a copy of the "Miele.log" found inside the docker container and place the file in the destination set within the script. I then automate this process to run every night by running the following again on the host machine:
 ```bash
 crontab -e
 ```
 then create the cronjob that  will run the backup script every night at 11:55 pm
 ```bash
 # m h  dom mon dow   command
 55 23  *   *   *     ~/projects/Miele/log_backup.sh
 ```

## Goals

The following are goals for this project and possible additions in the future:

- Further experience with Docker
- Further experience with shell scripts
- A basic honeypot to further develop
- A source of interesting data from users caught in the honeypot(maybe some graphing in D3)
