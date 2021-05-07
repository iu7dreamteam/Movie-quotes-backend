#!/bin/bash

docker pull sansanchezzz/movie-quotes:latest
docker rm -f $(docker ps -aq)
cd backend
docker-compose up -d --force-recreate