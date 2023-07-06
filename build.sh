#!/bin/bash

# Jump to "self" folder
cd "$(dirname "$0")"

# Init .env
docker-compose --env-file .env -f docker-compose.yml build --force-rm
docker image prune -f
