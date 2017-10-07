# A demo of high availability architecture
Make a demo for high availability architecture. 

## How to run

1. Create a db 'myapp' in mysql

2. Run the commands

First time: 
```bash
# fill the environment variables first
cp .env.dist .env
# run docker-compose
docker-compose up
# init the db table
docker exec -it my_uwsgi bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

3. Visit `localhost:8000/api/property` with GET and POST requests. 

## High availability architecture (typical)

Usually, we can have 6 layers in a web system: 

1. client: browser/app => dns-server
2. reverse proxy: system entrance
3. web app: core app logic, return html/json
4. service: provide core services
5. data-cache: speedup reads
6. data-db: persistence

The solution is to use `cluster/redundancy` + `failover`. 

NOTE: Usually, there is nothing much we can do in layer 1. But if we can set multiple IPs for a domain name, it can scale horizontally by adding more nginx servers. 

## Todo List

So I will follow the architecture from layer 2 to 6 and make each layer become high available: 

Plan: 
* [DONE] client -> reverse proxy: add another nginx as a backup and failover
* reverse proxy -> web+service: when a web server dies, nginx will redirect all traffic to other servers
* web+service -> data-cache: (1) double reads & writes (2) redis-sentinel (3) if cache miss is allowed, put a load balancer in front of a group of cache servers (sharding by keys)
* web+service -> data-db: master-slave and multi-db. 

Improvements: 
* change to use `pipenv` instead of using requirements.txt
* service discovery and configuration updates

## History

### v2.0 - adding failover service for nginx

Four layers: 
- haproxy (this is added to export internal network address)
- nginx_master + nginx_slave (provide failover service)
- uwsgi
- db

Try to pause `my_nginx_master`: 

```bash
$ docker pause my_nginx_master
```

Check your log and you will find that my_nginx_slave will do a failover. 

Now, try to unpause `my_nginx_master`

```bash
$ docker unpause my_nginx_master
```

Check your log and you will find that my_nginx_master will take the leader again because it has higher priority. 

### v1.0 - a starting demo

Three layers: 
- nginx
- uwsgi
- db
