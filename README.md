# Epic Events

## Set up the environment

```shell
 python3 venv env
```
```shell
source env/bin/activate
``` 

## Set up the database

WARN : We use MySQL for this project
We work in local, so please before setting up the database for this project, be sure to have correctly installed MySQL
on your computer or using Docker.

An env file is necessary to connect to the database so let's create this env file at the root of the project:
```shell
touch .env
```

then you will need to set few variables:
- "DB_PORT" 
- "DB_USER"
- "DB_PASSWORD"
- "DB_NAME"
