## Build and Run
```
# Create .env file and populate manually missing information, e.g tokens for telegram and OpenAI communications
cp .env.example .env 

# Build Docker Images
docker-compose build

# Generate python documentation for sphinx server locally, you must do it to wake up the entire docker-compose
docker-compose run openai-bot-sphinx sphinx-apidoc -o source/code ../src
docker-compose run openai-bot-sphinx make html

# Wake up all services
docker-compose up
```

## Database
To explore database using pgadmin visit http://localhost:8050 and login using admin@mail.com admin credentials
Register a server connection to the database using these informations:
```
host --> openai-bot-database
port --> 5432
db --> default
username --> admin
psw --> s3cr3t
```

## Docs
Visit http://localhost:9001 to have a local view of Sphinx documentation after waking up docker compose services.
If you have already generated teh Docs and want to re-create it, follow these steps:
```
# to clean
sudo rm -rd docs/build
sudo rm -rf docs/source/code

# OR to fix generated file for editing 
sudo chmod -R 777 docs/*
```

To generate the Python Docs:
```
docker-compose run openai-bot-sphinx sphinx-apidoc -o source/code ../src
docker-compose run openai-bot-sphinx make html 
```

Wakeup all services
```
docker-compose up
```
