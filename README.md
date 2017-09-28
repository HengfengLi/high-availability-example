# A demo of high availability architecture
Make a demo for high availability architecture. 

## How to run

1. Create a db 'myapp' in mysql

2. Run the commands
```bash
# fill the environment variables first
cp .env.dist .env
# run docker-compose
docker-compose up
```

3. Visit endpoint `localhost:8000/api/property` with GET and POST requests. 
