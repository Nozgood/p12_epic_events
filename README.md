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


## Tests

### Unit tests
We use unittest to manage unit testing, all of these tests are stored in tests/ package at the root of the project

### Coverage
To manage coverage of the project, we use the python library `coverage`
Some commands that can be useful about coverage: 

- to generate a coverage file:
```shell
    python -m coverage run -m unittest discover tests/
```
the coverage file, called `.coverage` is stored at the root of the project

- to check the coverage in the terminal:
```shell
    python -m coverage report
```

- to check the coverage via a HTML file with more details:
```shell
    python -m coverage html
```
The HTML file will be store in a directory called htmlcov/ at the root of the project