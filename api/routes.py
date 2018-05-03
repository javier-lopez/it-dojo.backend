from flask import render_template, flash, redirect, url_for, request, abort, jsonify

from api import app, bcrypt
from api.tty import tty_pool
from api.models import TTY
from api.decorators import requires_auth

from sh import tty_controller
from datetime import datetime
from base64   import b64encode
from os       import path

# temporal imports ==================================================================
from random import randint
# app.logger.debug('index => user => None')
#====================================================================================

#____________________________________________________[ TTY CREATE ]
@app.route('/v0.1/tty/', methods=['POST'])
@app.route('/v0.1/tty',  methods=['POST'])
@requires_auth
def post_tty():
    valid_tty_request = (
        request.json
        or 'template' in request.json
        or 'username' in request.json
    )

    if not valid_tty_request:
        abort(400)

    template = request.json['template']
    username = request.json['username']

    if not 'dry_run' in request.json:
        #create ttys in advance for upcomming requests
        tty_pool(template, 3)
        tty = TTY.objects(template=template, active=False, dry_run=False,).first()
        if tty is None:
            stdout  = {}
            for line in tty_controller("create", template + "/docker-compose.yml").splitlines():
                if line.find(':') >= 0:
                    k,v = line.split(":",2) # split at first : produce max 2 items
                else:
                    k,v = ['stdout', line]  # split at first : produce max 2 items
                stdout.setdefault(k.strip(), v.strip())  # add to dict & split at . into list

            uri     = stdout["uri"]
            readme  = stdout["readme"]
            try:
                f      = open(readme, "r")
                readme = f.read()
            except:
                readme = path.basename(readme) + " file doesn't exists"
            readme  = b64encode(readme.encode('utf-8'))

            dry_run = False
        else:
            tty.active   = True
            tty.username = username
            tty.save()
            return jsonify({'tty': tty2json(tty)}), 201
    else:
        uri = u'tty-'                \
                + str(randint(0, 9)) \
                + str(randint(0, 9)) \
                + str(randint(0, 9))
        uri+= ".it-dojo.io"
        readme  = b64encode("README.md is missing".encode('utf-8'))
        dry_run = True

    new_tty = TTY(
                template = template,
                username = username,
                uri      = uri,
                readme   = readme,
                dry_run  = dry_run,
              ).save()

    return jsonify({'tty': tty2json(new_tty)}), 201

#____________________________________________________[ TTY READ ]
@app.route('/v0.1/tty/', methods=['GET'])
@app.route('/v0.1/tty',  methods=['GET'])
@requires_auth
def get_ttys():
    ttys = TTY.objects()
    return jsonify({'ttys': [tty2json(tty) for tty in ttys]})

@app.route('/v0.1/tty/<tty_id>/', methods=['GET'])
@app.route('/v0.1/tty/<tty_id>',  methods=['GET'])
@requires_auth
def get_tty(tty_id):
    try:
        tty = TTY.objects(id=tty_id).first()
        if tty is None:
            abort(404)
    except:
        abort(404)
    return jsonify({'tty': tty2json(tty)})

#____________________________________________________[ TTY UPDATE ]
@app.route('/v0.1/tty/<tty_id>/', methods=['PUT'])
@app.route('/v0.1/tty/<tty_id>',  methods=['PUT'])
@requires_auth
def update_task(tty_id):
    try:
        tty = TTY.objects(id=tty_id).first()
    except:
        abort(404)
    if tty is None:
        abort(404)
    if not request.json:
        abort(400)
    if 'template' in request.json and type(request.json['template']) != unicode:
        abort(400)
    if 'username' in request.json and type(request.json['username']) is not unicode:
        abort(400)
    if 'active' in request.json and type(request.json['active']) is not bool:
        abort(400)

    tty.template = request.json.get('template', tty.template)
    tty.username = request.json.get('username', tty.username)
    tty.username = request.json.get('active',   tty.active)
    tty.save()

    return jsonify({'tty': tty2json(tty)})

#____________________________________________________[ TTY DELETE ]
@app.route('/v0.1/tty/<tty_id>/', methods=['DELETE'])
@app.route('/v0.1/tty/<tty_id>',  methods=['DELETE'])
@requires_auth
def delete_task(tty_id):
    try:
        tty = TTY.objects(id=tty_id).first()
        if tty is None:
            abort(404)
    except:
        abort(404)

    if not tty.dry_run:
        image_id = tty.uri # tty-uu3js81.it-dojo.io
        image_id = image_id[4:image_id.index(".")] # uu3js81
        stdout   = tty_controller("delete", tty.template, image_id).splitlines()

    tty.delete()
    return jsonify({'result': True})

#____________________________________________________[ TTY ENV READ ]
@app.route('/v0.1/tty/env/', methods=['GET'])
@app.route('/v0.1/tty/env',  methods=['GET'])
@requires_auth
def get_envs():
    # stdout  = tty_controller(
        # "-T",
        # "../templates/",
        # "-L",
    # ).splitlines()
    # ./tty-controller -T ../templates/ -L
    # devops/linux/core-utils/docker-compose.yml
    # devops/conf_managers/terraform/docker-compose.yml

    # stdout  = [
        # "devops/linux/core-utils/docker-compose.yml",
        # "devops/conf_managers/terraform/docker-compose.yml",
    # ]

    # stdout  = [
        # "devops",
        # "webdev",
        # "bigdata",
    # ]

    stdout  = {
        "devops": [
            "linux/core-utils",
            "conf_managers/terraform",
        ],
        "webdev" : [],
        "bigdata": [],
    }

    return jsonify({'envs': stdout})

@app.route('/v0.1/tty/env/<env_id>/', methods=['GET'])
@app.route('/v0.1/tty/env/<env_id>',  methods=['GET'])
@requires_auth
def get_env(env_id):
    # stdout  = tty_controller(
        # "-T",
        # "../templates/",
        # "-L",
    # ).splitlines()
    # ./tty-controller -T ../templates/ -L
    # devops/linux/core-utils/docker-compose.yml
    # devops/conf_managers/terraform/docker-compose.yml

    stdout  = {
        "devops": [
            "linux/core-utils",
            "conf_managers/terraform",
        ],
        "webdev" : [],
        "bigdata": [],
    }

    env = None

    try:
        env = stdout[env_id]
        if env is None:
            abort(404)
    except:
        abort(404)

    return jsonify({'env': env})

##############################################################################

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(400)
def not_found(error=None):
    message = {
        'status': 400,
        'message': 'Bad request',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(405)
def not_found(error=None):
    message = {
        'status': 405,
        'message': 'Method not allowed for: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 405
    return resp

def tty2json(tty):
    formatted_tty = {}
    for field in tty:
        if field == 'id':
            #replace id field for a control uri
            formatted_tty['endpoint'] = url_for(
                'get_tty', tty_id=tty['id'], _external=True)
        elif field == 'created':
            formatted_tty['created'] = tty['created'].__str__()
        elif field == 'destroyed':
            formatted_tty['destroyed'] = tty['created'].__str__()
        else:
            formatted_tty[field] = tty[field]
    return formatted_tty
