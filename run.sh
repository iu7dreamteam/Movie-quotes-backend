#!/bin/bash

docker pull sansanchezzz/movie-quotes:latest
docker rm -f $(docker ps -aq)
cd backend
docker-compose up -d --force-recreate
docker-compose exec web python3 manage.py migrate