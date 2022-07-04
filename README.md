# Project abyssinian
A test api application created for improving skills with the following stack:
 - FastAPI
 - SQLAlchemy
 - Alembic
 - Github Actions
 - AWS (Lambda, S3, CloudFormattion, Cognito)
 - Terraform


## Requirements (Prerequisites)

Tools and packages required to successfully install this project.

- GNU Make >= 3.81 [Install](https://www.gnu.org/software/make)
- Git >= 2.35.1 [Install](https://git-scm.com/downloads)
- Docker >= 20.10.16 [Install](https://docs.docker.com/get-docker/)
- Docker Compose >= v2.2.3 [Install](https://docs.docker.com/compose/install/)

If you are running in virtual environment, following packages are also required.

- Python >= 3.10.1 [Install](https://www.python.org/downloads/)
- Postgres == 12.5 [Install](https://www.postgresql.org/download/)

## Installation
### Setup
A step by step list of commands/guide that informs how to install/run an instance of this project.

Clone the repository and cd into it.
```shell
git clone https://github.com/oswalth/abyssinian.git
cd abyssinian
```

Copy `.env.dev` file into `.env` file. Optionally, configure the environment variables with your own values.
```shell
cp .env.dev .env
```

Build docker images with
```shell
docker-compose up -d --build app
```

Confirm that the project is running.
```shell
make ps

      Name                    Command               State           Ports         
----------------------------------------------------------------------------------
abyssinian_app_1   /app/entrypoint.sh poetry  ...   Up      0.0.0.0:9050->9050/tcp
abyssinian_db_1    docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
```

Open the system status page at [http://localhost:9050/ping](http://localhost:9050/ping).
