# Epic Events

## Set up the environment

```shell
 python3 venv env
```
```shell
source env/bin/activate
``` 

## Set up the database

WARN : We use Postgres for this project
We work in local, so please before setting up the database for this project, be sure to have correctly installed Postgres
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

## Run

To run the project, in the terminal, at the root of the project, once you correctly set up and activate the virtual environment :
```shell
python main.py 
```

Then, just let the terminal speaks with you :D 

### Migrations

To manage migrations we use alembic, if you correctly installed it should be already available in your env
But if you want to install this tool by yourself: 
```shell
pip install alembic
```
If you want to change the database on which you will do your migrations, don't forget to edit the `alembic.ini` file 
and set the variable `sqlalchemy.url`

**How Alembic runs ?**

When you will do a change on the models, run this command in the terminal, at the root of the project:
```shell
alembic revision --autogenerate -m "Description of the change"
```

It will generate a migration file in the directory `migrations/versions`

Then, when you're ready to process the migration:
```shell
alembic upgrade head
```

WARN: Migrations can make huge damages to the DB if they are not correctly managed, please be careful when you set one

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
