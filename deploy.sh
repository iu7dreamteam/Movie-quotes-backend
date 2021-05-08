#!/bin/bash
cd /var/www/movie-quotes.ru/api
docker-compose stop
docker-compose rm -f
docker pull sansanchezzz/movie-quotes:latest
docker-compose up -d --force-recreate
docker-compose exec -T web python3 manage.py migrate
