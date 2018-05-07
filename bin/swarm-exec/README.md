Taken shameless from https://github.com/opsani/skopos-plugin-swarm-exec

# Usage

    $ docker run -v /var/run/docker.sock:/var/run/docker.sock opsani/skopos-plugin-swarm-exec task-exec <taskID> <command> [<arguments>...]

Or on Ubuntu:

    $ apt-get install -y --no-install-recommends python-pip python-setuptools curl python3 python3-requests python3-setuptools python3-pip
    $ pip3 install --upgrade pip
    $ pip3 install docker
    $ ./swarm-exec task-exec <taskID> <command> [<arguments>...]

Or on Alpine:

    $ apk -U add python3
    $ pip install requests docker
    $ ./swarm-exec task-exec <taskID> <command> [<arguments>...]

Where <taskID> is generated by:

    $ docker [stack|service] ls
    $ docker [stack|service] ps <stack_name> --format "{{.ID}} {{.Name}} {{.Image}} {{.Node}} {{.DesiredState}} {{.CurrentState}}" | awk '{print $1}'