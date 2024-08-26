# `python-social-media`

Demo very very simple social media application with Python and Django :)

## Django setting setup

1. Settings reference from [Django-Styleguide](https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#settings)

## API Server Feature

1. user create
2. chatroom create
3. chatroom get
4. chatrooms of user
5. chatroom join
6. message create
7. messages of room
8. message delete

## Websocket Server Gateway

1. Consume message from API server with rabbitmq.


## Local setup

### apiserver project

1. dynamodb: `python3 manage.py runscript migrate_dynamodb_local_script`
2. database: `CREATE DATABASE socialmedia;`
3. runserver: `python3 manage.py runserver 8000`

### apiserver .env file

```
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

JWT_SECRET_KEY=your_jwt_secret_key
JWT_EXPIRATION_DELTA_SECONDS=3600
JWT_ISSUSER=python-socialmedia

DATABASE_NAME=socialmedia
DATABASE_USER=root
DATABASE_PASSWORD=secret
DATABASE_HOST=localhost
DATABASE_PORT=3306

AWS_DYNAMODB_LOCAL=http://localhost:8080
AWS_REGION_NAME=ap-east-1

RABBITMQ_SCHEME=amqp
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
```

### wsgatewayserver project

1. runserver: `python3 manage.py runserver 8001`

### wsgatewayserver .env file

```
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True

JWT_SECRET_KEY=your_jwt_secret_key
JWT_EXPIRATION_DELTA_SECONDS=3600
JWT_ISSUSER=python-social-media

RABBITMQ_SCHEME=amqp
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
```

## Dependencies

1. Django
2. Django-ninja
3. channels
4. Mysql
5. DynamoDB
6. PyJWT
7. RabbitMQ
8. Pika
9. 
## Todo list in future

1. Insert message delata data to search engine database(e.g Elasticsearch) with CDC concept.
2. Implement message full-text search logic.
3. Implement cache system.
4. Implement test case.
5. Authorizate websocket connection.
6. Implement message dispatcher.
7. more ...
