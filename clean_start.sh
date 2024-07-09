#!/bin/bash
docker-compose down
docker system prune -a -f --volumes
docker-compose build --no-cache
docker-compose up