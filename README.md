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

3. Visit endpoint `localhost:8000/api/property` with GET and POST requests. 
