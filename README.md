# DgxInfo
User's Docker container information

https://hub.docker.com/r/falconjk/dgxinfo

![](https://i.imgur.com/UZgCNUR.png)
## Used
* docker-py 
* Flask
* uWSGI
* NGINX

## docker run command
`docker run -idt --restart=always --cpus=2 --name dgxinfo -v /var/run/docker.sock:/var/run/docker.sock -p 80:80 falconjk/dgxinfo`

## Connect 
* http://{ip}/{username}
* example: http://192.168.0.2/bob