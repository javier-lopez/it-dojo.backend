# Quick Start

Provides/decommise web tty instances on demand, using docker-swarm
infraestructure + traefik tagging + ingress routing.

To download this repository use:

    $ git clone --recursive https://github.com/it-dojo/it-dojo.backend

If you already downloaded the repository without the submodules, use the
following to correct:

    $ git submodule update --init --recursive

## Setup local environment

    $ echo  'passwd' > .vault_pass.txt #never add the .vault_pass.txt file to git!
    $ touch .env #never add the .env content to git!
    $ vagrant plugin install vagrant-hostmanager-ext vagrant-triggers
    $ vagrant up --provision #takes 15-60 mins depending on your connection

    $ ANSIBLE_ARGS='--tags api' vagrant up --provision #for subsecuent runs

## Setup dev environment

    $ ./setup.sh [docker-compose-file] #require docker + docker-compose

### Sample interactions

    # GET ALL DISPATCHED TTYs, NO AUTHENTICATION
    $ curl -L -k -i api.it-dojo.io/v0.1/tty/
      HTTP/1.0 401 UNAUTHORIZED

    # GET ALL DISPATCHED TTYs, AUTHENTICATED
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/
      HTTP/1.0 200 OK

    # GET TTY DETAILS
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/<id>
      HTTP/1.0 200 OK

    # GET AVAILABLE ENVIRONMENTS
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/env/
      HTTP/1.0 200 OK

    # GET ENVIRONMENT DETAILS
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/env/<id>
      HTTP/1.0 200 OK

    # RUN TTY TESTS
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/<id>/test
      HTTP/1.0 200 OK

    # RUN SPECIFIC TTY TESTS
    $ curl -L -k -i -u "admin:admin"        \
        -H "Content-Type: application/json" \
        -X POST                             \
        -d '{"script":"echo"}'              \
        api.it-dojo.io/v0.1/tty/<id>/test
      HTTP/1.0 200 OK

    # REQUEST NEW TTY (requires docker swarm enabled)
    $ curl -L -k -i -u "admin:admin"        \
        -H "Content-Type: application/json" \
        -X POST                             \
        -d '{"username":"user@it-dojo.io", "template": "devops/linux/core-utils"}' \
        api.it-dojo.io/v0.1/tty
      HTTP/1.0 201 CREATED

    # REQUEST NEW TTY, DRY RUN MODE (doesn't require docker swarm enabled)
    $ curl -L -k -i -u "admin:admin"        \
        -H "Content-Type: application/json" \
        -X POST                             \
        -d '{"username":"user@it-dojo.io", "template": "devops/linux/core-utils", "dry_run": true}' \
        api.it-dojo.io/v0.1/tty
      HTTP/1.0 201 CREATED

    # REMOVE TTY
    $ curl -L -k -i -u "admin:admin" -X DELETE api.it-dojo.io/v0.1/tty/<id>
      HTTP/1.0 200 OK
