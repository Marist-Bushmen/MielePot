# MIELE POT
# Author:  Daniel Nicolas Gisolfi

DEV_HOME=./src
DOCKER_IMAGE=dgisolfi/mielepot
APPNAME=mielepot

#####################
# Common Commands
#####################

intro:
	@echo "\n					MielePot"



#####################
# Docker Commands
#####################


docker_image:
	@# Initial commands used priming devops environment
	@# Note: If docker account "dan36911" is not used; This command required
	@echo "\n				Creating mielepot docker image"
	@# @ln -s /Users/daniel/code-repos/Blockchain/lib /Users/daniel/code-repos/Blockchain/src
	@docker build -t mielepot .

dev_container:
	@# This command should be run from the local computer
	@echo "\n Creating Docker container"
	@#dq;elrkgsocker pull ${DOCKER_IMAGE}
	@#wenfdocker run -it --name bushmen_devtest --rm -p 80:80 -v ${PWD}:/DNG ${DOCKER_IMAGE} bash
	@#docker run --rm -p 800:80 -v /Users/daniel/code-repos/MielePot/src:/var/www/html/ mielepot
	@sudo docker-compose run web django-admin.py startproject mielepot .
publish_image: docker_image
	@echo "\n				Create MielePot docker image..."
	@#docker login
	@docker tag mielepot ${DOCKER_IMAGE}:latest
	@docker push ${DOCKER_IMAGE}
