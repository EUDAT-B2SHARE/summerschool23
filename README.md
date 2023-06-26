# EUDAT summer school B2SHARE training
This repository contains Docker Compose definitions for B2SHARE deployment to be used for EUDAT summer school activities.

## Installation
```
# Edit B2SHARE configuration as instructed
micro b2share.env

# Docker Compose automatically uses .env file
cp b2share.env .env

# Start support services B2SHARE needs
docker compose up -d

# Initialize database and search index (when setting up the instance for the first time)
docker compose run --rm b2share-init

# Start B2SHARE
docker-compose --profile b2share up -d
```


## Useful links

 * [B2SHARE documentation](https://docs.eudat.eu/b2share)
 * [B2SHARE training module](https://github.com/EUDAT-Training/B2SHARE-Training/tree/master/deploy)
 * [B2SHARE install notes](https://github.com/EUDAT-B2SHARE/b2share/blob/evolution/INSTALL.rst)

