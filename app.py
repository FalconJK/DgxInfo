import time

import requests
from docker import Client
from flask import Flask, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def ip():
    return requests.get('http://ifconfig.me/ip').text.strip()


@limiter.limit("200 per hour")
@app.route('/json')
def json(name=None):
    start = time.time()
    host = Client(base_url='unix://var/run/docker.sock')
    print('\nprocess time:', time.time() - start, '\n')
    return jsonify(host.containers(all=True))


@limiter.limit("200 per hour")
@app.route('/<name>')
def template(name=None):
    start = time.time()
    host = Client(base_url='unix://var/run/docker.sock')
    host_containers = host.containers(all=True)
    all_containers = [container['Names'][0].replace('/', '') for container in host_containers]
    all_user_containers = [container for container in all_containers if '_' in container]
    #     -----------------------------------------------------------------------------------------------
    user_list = set([container.split('_')[0] for container in all_user_containers])
    if name in user_list:
        specific_user_containers = [container for container in all_containers if name in container]
    else:
        specific_user_containers = list()
    #     -----------------------------------------------------------------------------------------------
    names = [container.pop('Names')[0].replace('/', '') for container in host_containers]
    api = dict(zip(names, host_containers))
    new_api = api.copy()
    for container_name in api:
        if container_name not in specific_user_containers:
            del new_api[container_name]
    del api, all_user_containers, specific_user_containers, all_containers

    for container, data in new_api.items():
        context = list()
        ports = sorted(data['Ports'], key=lambda p: p['PrivatePort'])

        for port in ports:
            private_port = port.get('PrivatePort')
            public_port = port.get('PublicPort')
            public = ''
            if port.get('IP') != None:
                public = f"{port['IP']}:{public_port}->"
            private = f"{port['Type']}/{private_port}, "
            NAT = public + private
            if private_port != 8888 and private_port != 6080:
                context.append(NAT)
            else:
                new_api[container]['jupyter_link'] = f'http://{ip()}:{public_port}'
                new_api[container]['jupyter_text'] = NAT[:-2]

        new_api[container]['Ports'] = ''.join(context)
    running = 0
    for i in new_api:
        if new_api[i]['State'] == 'running':
            running += 1
    return render_template('index.html', name=name, running=running, total=len(new_api), containers=new_api.items())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
