SHELL := /bin/bash
PROJECT_NAME := finish-lynx-my
IMAGE_NAME := $(PROJECT_NAME):latest

all:
	@echo "build run stop logs"

build:
	@docker build -t $(IMAGE_NAME) .
	

run:
	@docker stop $(PROJECT_NAME) || true
	@docker rm $(PROJECT_NAME) || true
	@docker run \
		-d \
		--name $(PROJECT_NAME) \
		--network host \
		--env-file .env \
		--restart=unless-stopped \
		$(IMAGE_NAME)
	
stop:
	@docker stop $(PROJECT_NAME) || true
	

logs:
	@docker logs -f $(PROJECT_NAME)
