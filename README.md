# MielePot
A basic honeypot to gather data on attempted logins, to be expanded on for further data collection. Currently, the honeypot is running at [dgisolfi.xyz:4400](http://dgisolfi.xyz:4400/)

### Authors

**Daniel Gisolfi** - *All current work* - [dgisolfi](https://github.com/dgisolfi)

## Prerequisites

All requirements to run an instance of this project

- A VM with root access
- Bootstrap 4(not needed but used for login form)
- Docker(and Docker Compose)
- Flask

## Docker Implementation

The honeypot takes advantage of Docker containers and is run using the image pulled from docker hub. The image for this honeypot can be found [here](https://hub.docker.com/r/dgisolfi/mielepot/). The Dockerfile found in the source directory of this repository is used to create the miele image. The Docker file does the following:
1. pull the latest version of Ubuntu from docker hub
2. install the following: python-pip, python-dev, build-essential
3. Create a directory in the image, and copy all of src into it
4. install all python requirements
5. define the entry-point and command to run on startup



# Miele Setup

## Container setup

Using Docker Compose you can boot all predefined services in parallel, the Docker Compose file found in the root directory of this repository is written to create a Postgres database as well as an instance of miele for you. 

The following is a basic guide on how to deploy the miele honeypot. Start by placing docker compose YAML file and the log_backup script from the repository into your production environment. After ensuring Docker is installed on the machine with the correct user access given and that the shell script is executable, run the following in the directory containing the two files:

```bash
docker-compose up
```

Running this command should automatically pull the latest version of miele as well as the latest version of Postgres and boot the containers with all necessary data. To see the running container execute the following in any directory on the host machine
```bash
docker ps -a
```
You will see a list of running and any exited containers, our honeypot is the one named "miele_prod". At this point, you should be able to go to the IP address of the machine running this container and see the honeypot on port 4400. If running on a local machine visit [localhost](http://0.0.0.0:4400)

## Logging setup
The Docker container is set up to log all requests to the site. However with Docker containers unless volumes are used all data is lost once the container is killed. At any point, while a container is running you may enter the bash shell for that particular container, to do so run the following on the host machine
```bash
docker exec -it miele_prod bash
```

In order to save the logs recorded by the honeypot, a system must be set up to copy the file over to the host machine. This can be done in many ways however I chose to use a cronjob with a bash script. The bash script that was initially placed on the host machine will be used to do this. In the script edit the variable that sets the path to where logs will be saved. In my case, I created a directory called logs at the level of the bash script. When running, the bash script will create a copy of the "MIE02-DATE.log" found inside the docker container and place the file in the destination set within the script. I then automate this process to run every hour on the 10th minute by running the following on the host machine:
 ```bash
 sudo crontab -e
 ```
 then create the cronjob that  will run the backup script every hour on the 10th minute
 ```bash
 # m h  dom mon dow   command
  10 *  *   *   *     ~/projects/miele/log_backup.sh
 ```

## Goals

The following are goals for this project and possible additions in the future:

- Further experience with Docker
- Further experience with bash scripts
- A basic honeypot to further develop
- A source of interesting data from users caught in the honeypot(maybe some graphing in D3)
