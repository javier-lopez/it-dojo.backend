# Quick Start

## Setup local environment

    $ echo 'passwwd' > .vault_pass.txt #never add the .vault_pass.txt file to git!
    $ vagrant plugin install vagrant-hostmanager-ext
    $ vagrant up --provision #takes 15-60 mins depending on your connection

    $ ANSIBLE_ARGS='--tags api' vagrant up --provision #for subsecuent runs

API provides/decommise web tty instances on demand, using docker-swarm
infraestructure + traefik tagging + ingress routing

### Sample interactions

    # GET ALL DISPATCHED TTYs, NO AUTHENTICATION
    $ curl -L -k -i api.it-dojo.io/v0.1/tty/
      HTTP/1.0 401 UNAUTHORIZED

    # GET ALL DISPATCHED TTYs, AUTHENTICATED
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/
      HTTP/1.0 200 OK

    # GET SPECIFIC TTY
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/3
      HTTP/1.0 200 OK

    # GET INVALID TTY
    $ curl -L -k -i -u "admin:admin" api.it-dojo.io/v0.1/tty/999999
      HTTP/1.0 404 NOT FOUND

    # REQUEST NEW TTY
    $ curl -L -k -i -u "admin:admin"        \
        -H "Content-Type: application/json" \
        -X POST                             \
        -d '{"username":"foobar@it-dojo.io", "template": "tty-base"}' \
        api.it-dojo.io/v0.1/tty
      HTTP/1.0 201 CREATED

    # REMOVE TTY
    $ curl -L -k -i -u "admin:admin" -X DELETE api.it-dojo.io/v0.1/tty/1
      HTTP/1.0 200 OK


## Setup dev environment

    $ ./setup.sh #require docker + docker-compose

### Sample interactions

    # GET ALL DISPATCHED TTYs, NO AUTHENTICATION
    $ curl -i http://localhost:5000/v0.1/tty/
      HTTP/1.0 401 UNAUTHORIZED

    # GET ALL DISPATCHED TTYs, AUTHENTICATED
    $ curl -i -u "admin:admin" http://localhost:5000/v0.1/tty/
      HTTP/1.0 200 OK

    # GET SPECIFIC TTY
    $ curl -i -u "admin:admin" http://localhost:5000/v0.1/tty/3
      HTTP/1.0 200 OK

    # GET INVALID TTY
    $ curl -i -u "admin:admin" http://localhost:5000/v0.1/tty/999999
      HTTP/1.0 404 NOT FOUND

    # REQUEST NEW TTY
    $ curl -i -u "admin:admin"              \
        -H "Content-Type: application/json" \
        -X POST                             \
        -d '{"username":"foobar@it-dojo.io", "template": "tty-base"}' \
        http://localhost:5000/v0.1/tty
      HTTP/1.0 201 CREATED

    # REMOVE TTY
    $ curl -i -u "admin:admin" -X DELETE http://localhost:5000/v0.1/tty/1
      HTTP/1.0 200 OK
