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
* [DONE] reverse proxy -> web+service: when a web server dies, nginx will redirect all traffic to other servers
* [DONE] web+service -> data-cache:
    1. double reads & writes 
    2. redis-sentinel [USE]
    3. if cache miss is allowed, put a load balancer in front of a group of cache servers (sharding by keys)
* web+service -> data-db: master-slave and multi-db. 

Improvements: 
* change to use `pipenv` instead of using requirements.txt
* service discovery and configuration updates

## History

### v4.0 - adding cache layer

- Add cache layer
- Use `wrk` to test the improvement of performance
- Make cache layer highly available
- Use `docker-compose --scale [SERVICE=NUM]` to run more containers  and needs to remove container_name

Performance Test:

```bash
wrk -c 100 -t 12 -d 5s http://127.0.0.1:8000/api/property
```

Without cache:

```bash
Running 5s test @ http://127.0.0.1:8000/api/property
  12 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.16s   386.38ms   1.98s    64.42%
    Req/Sec     7.88      5.47    30.00     76.64%
  340 requests in 5.08s, 1.30MB read
  Socket errors: connect 0, read 5, write 0, timeout 14
Requests/sec:     66.92
Transfer/sec:    261.72KB
```

With cache:

```bash
Running 5s test @ http://127.0.0.1:8000/api/property
  12 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   407.86ms  235.19ms   1.46s    69.11%
    Req/Sec    20.84     13.66    90.00     79.84%
  1168 requests in 5.07s, 3.79MB read
  Socket errors: connect 0, read 28, write 0, timeout 0
Requests/sec:    230.58
Transfer/sec:    765.84KB
```

With cache, the latency is much less and more requests can be processed.

Actually, we can use `docker-compose scale` command to scale the number of
containers:

```bash
docker-compose up --scale uwsgi=3 --scale redis_slave=2 --scale redis_sentinel=3
```

### v3.0 - using nginx as HTTP load balancer

Notes: 
- I tried to use `docker swarm`, but `cap_add` for virtual IP and keepalived is not supported. So I have to find an alternative way to do this. 
- For now, I just manually add 3 web app servers and use nginx as load balancer. 
- Change to use http instead of using socket files. 
- Need to use `upstream` directives `max_fails` and `fail_timeout`
- Use `docker stop` to kill a container instead of using `docker pause`.  `docker pause` is not working and it seems that container still can be pinged. 

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

Check your log and you will find that `my_nginx_slave` will do a failover. 

Now, try to unpause `my_nginx_master`

```bash
$ docker unpause my_nginx_master
```

Check your log and you will find that `my_nginx_master` will take the leader again because it has higher priority. 

### v1.0 - a starting demo

Three layers: 
- nginx
- uwsgi
- db
