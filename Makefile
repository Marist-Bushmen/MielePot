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
	@docker build -t mielepot ./src/.

publish_image: docker_image
	@echo "\n				Create MielePot docker image..."
	@#docker login
	@docker tag mielepot ${DOCKER_IMAGE}:latest
	@docker push ${DOCKER_IMAGE}
