# ts-graph-builder-backend

# Description
Grapher's backend which uses a docker container to store data in mongodb and a python api for microservices.

# Quick start

Install docker if you have not
https://docs.docker.com/engine/install/

```bash
# Run docker compose to start the mongodb container.
docker compose up -d
```

Install python and its requirements

```bash
# Install python packages from requirements.txt
pip install -r requirements.txt
```

# Mongodb database
The docker container runs mongo-express as well, allowing easy manipulation and viewing of the graph datasets.
The web-ui offers quick ways to create new databases, collections and graphs.