# django-dokku-deployment-demo

This project demonstrates how to deploy a simple Django project to [Dokku](https://dokku.com/).

It is served at https://d4.ebmdatalab.net/.

## Setup

### DNS

DNS is managed through Cloudflare (login details in Bitwarden).

I created a new A record for `d4.ebmdatalab.net`, with IP address `157.245.31.108`.
Initially, the record must be "DNS only", and not proxied.
This is to allow the creation of a certificate with Let's Encrypt.

### Setting up dokku

After SSHing to `dokku2` and switching to the `dokku` user, I ran:

* `dokku apps:create d4`
* `dokku domains:add d4 d4.ebmdatalab.net`
* `dokku git:set d4 deploy-branch main`
* `dokku letsencrypt:enable d4`
* `mkdir /var/lib/dokku/data/storage/d4`
* `dokku storage:mount d4 /var/lib/dokku/data/storage/d4/:/storage`
* `dokku config:set d4 SECRET_KEY=$(openssl rand -base64 48)`

After running `letsencrypt:enable`, I enabled proxying in Cloudflare.

### The Git remote

Deploying is done via pushing the git repo to a remote on `dokku2`.
To set this up, I ran:

* `git remote add dokku dokku@dokku2:d4`

## Deploying

To deploy, run:

* `git push dokku`

On deploy, a docker container is built using the `Dockerfile` in this repo,
and the commands in `entrypoint.sh` are run.

## Management commands

To run a management command against the deployed site, run the following as the `dokku` user on `dokku2`:

* `dokku enter d4`
* `./manage.py ...`

## TODO

* automatically deploying on merge
* building/serving static files
