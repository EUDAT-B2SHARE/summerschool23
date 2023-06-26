# EUDAT summer school B2SHARE training
This repository contains Docker Compose definitions for B2SHARE deployment to be used for EUDAT summer school activities.

In this training you will:
- set-up your B2SHARE instance on a VM created for you.
- configure and administrate your B2SHARE service

### Instance set-up

!!! Commands should be run in the VM given to you at the start of the training.

Clone GH repo
``` bash
git clone https://github.com/EUDAT-B2SHARE/summerschool23.git /home/ubuntu/summerschool23
cd /home/ubuntu/summerschool23
```

Edit b2share.env
- Change value of B2SHARE_JSONSCHEMAS_HOST to match your instance hostname
``` bash
cp b2share.env .env
micro .env
```

#### Certificates for NGINX

Create a directory for storing TLS cert for  NGINX Docker Container
``` bash
mkdir -p /home/ubuntu/summerschool23/data/nginx-data/ssl/
```

Copy Let's Encrypt certificates to /home/ubuntu/summerschool23/data/nginx-data/ssl
(Certificates have been obtained for you)
``` bash
cp ~/fullchain.pem /home/ubuntu/summerschool23/data/nginx-data/ssl/b2share.crt
cp ~/privkey.pem /home/ubuntu/summerschool23/data/nginx-data/ssl/b2share.key
```

#### Docker Image preparation (OPTIONAL)

Build Docker Images
```bash
sudo docker compose build elasticsearch nginx
```

Pull Docker Images
``` bash
sudo docker compose pull postgres mq redis b2share-base
```

#### Start B2SHARE and services it needs.

Start service dependencies
``` bash
sudo docker compose up -d
```

Initialize PostgreSQL database and Elasticsearch search Index.
Initialization needs to be done just once on a fresh deployment.
``` bash
sudo docker compose run --rm b2share-init
```

Start B2SHARE
```bash
sudo docker compose --profile b2share up -d
```

!!! At this point you can check your B2SHARE deployment by accessing it over HTTPS in your web browser.
Instance should not contain any content (e.g. records, communities)

Create some demo content with a Python script.
(script is in `./demo/add_eudat_community.py`)
```bash
sudo docker compose run --rm b2share-demo
```

#### Useful commands

You can monitor logs from all containers with following command.
```bash
sudo docker compose --profile b2share logs -f
```

You can "reset" your instance by destroying database and search index content.
Remember to init after reset.
```bash
sudo docker compose run --rm b2share-reset
```


### B2SHARE Service set-up and administration

Cannot login to your instance via B2ACCESS.
- Update your B2SHARE configuration with your B2ACCESS ***OIDC client credentials*** created in a previous training session.
  (`B2ACCESS_CONSUMER_KEY` and `B2ACCESS_SECRET_KEY` variables in your `.env` file)
- Update your B2ACCESS OIDC client configuration with ***redirect url*** for your B2SHARE instance.
  (Done in B2ACCESS web UI)
- Restart B2SHARE with `sudo docker compose --profile b2share up -d`

#### Create your own community

First open a bash prompt inside a B2SHARE container
```bash
sudo docker compose run --rm b2share-tools
```

Then create a community with following command
(path `./demo/` is already mounted to the container with summer.png logo.)
```bash 
b2share communities create -v "Summer School 2023" "Community for Summer School 2023" "/eudat/b2share/webui/app/img/communities/summer.png"
```

You must assign a metadata schema for the created community.
Example schema from `./demo/` folder is already mounted to container.
```bash
b2share communities set_schema "Summer School 2023"
```

Now you can create records for the new community.

#### Change settings via config.py method

A `config.py` file is bind mounted to B2SHARE containers in `docker-compose.yml`.
This file contains additional configuration values for B2SHARE which cannot be defined via environment variables.
For example, in order to enable creation of fake, nonresolvable Datacite DOIs and EPIC PIDs you can edit the mounted `config.py` file and then reload the B2SHARE services. Note that in a real production deployment the whole Docker Compose stack would not be brought down, but B2SHARE would be reload via other means.

Start by editing 'FAKE_EPIC_PID' and 'FAKE_DOI' variables in `config.py`.
(e.g `# FAKE_EPIC_PID = False` to `FAKE_EPIC_PID = True`)
```bash
micro ./demo/config.py
```

Then reload the Docker Compose stack
```bash
sudo docker compose --profile b2share down
sudo docker compose --profile b2share up -d
```

Once B2SHARE has fully started you can create a record and check if it gets a fake EPIC PID and DOI.


## Useful links

 * [B2SHARE documentation](https://docs.eudat.eu/b2share)
 * [B2SHARE training module for deployment](https://github.com/EUDAT-Training/B2SHARE-Training/tree/master/deploy)
