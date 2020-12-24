#! /bin/bash
docker rm -f dgxinfo
docker rmi dgxinfo:v1.0.0
docker build -t dgxinfo:v1.0.0 .
docker run -it --restart=always --cpus=2 --name dgxinfo -v /var/run/docker.sock:/var/run/docker.sock -p 81:80 dgxinfo:v1.0.0
