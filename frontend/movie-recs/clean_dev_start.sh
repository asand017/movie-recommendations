#!/bin/bash
# docker system prune -a -f --volumes
docker build -t nextjs-app-dev .
docker run -p 3000:3000 -v $(pwd):/app -v /app/node_modules nextjs-app-dev