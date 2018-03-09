from flask import render_template, flash, redirect, url_for, request, abort, jsonify

from api import app, bcrypt
from api.tty import tty_pool
from api.models import TTY
from api.decorators import requires_auth

from sh import tty_controller
from datetime import datetime

# temporal imports ==================================================================
from random import randint
#====================================================================================

#____________________________________________________[ CREATE ]
@app.route('/v0.1/tty/', methods=['POST'])
@app.route('/v0.1/tty',  methods=['POST'])
@requires_auth
def post_tty():
    if not request.json or not 'template' in request.json or not 'username' in request.json:
        abort(400)

    if not 'dry_run' in request.json:
        tty_pool(request.json['template'], 3) #create ttys in advance for upcomming requests
        tty = TTY.objects(template=request.json['template'], active=False, dry_run=False).first()
        if tty is None:
            output  = tty_controller("create",  request.json['template'] + ".yml").splitlines()
            uri     = output[-1]
            dry_run = False
        else:
            tty.active   = True
            tty.username = request.json['username']
            tty.save()
            return jsonify({'tty': format_reply(tty)}), 201
    else:
        uri     = u'tty-' + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        uri    += ".it-dojo.io"
        dry_run = True

    new_tty = TTY(
                template = request.json['template'],
                username = request.json['username'],
                uri      = uri,
                dry_run  = dry_run,
              ).save()

    return jsonify({'tty': format_reply(new_tty)}), 201

#____________________________________________________[ READ ]
@app.route('/v0.1/tty/', methods=['GET'])
@app.route('/v0.1/tty',  methods=['GET'])
@requires_auth
def get_ttys():
    ttys = TTY.objects()
    return jsonify({'ttys': [format_reply(tty) for tty in ttys]})

@app.route('/v0.1/tty/<tty_id>/', methods=['GET'])
@app.route('/v0.1/tty/<tty_id>',  methods=['GET'])
@requires_auth
def get_tty(tty_id):
    try:
        tty = TTY.objects(id=tty_id).first()
    except:
        abort(404)
    if tty is None:
        abort(404)
    return jsonify({'tty': format_reply(tty)})

#____________________________________________________[ UPDATE ]
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

    return jsonify({'tty': format_reply(tty)})

#____________________________________________________[ DELETE ]
@app.route('/v0.1/tty/<tty_id>/', methods=['DELETE'])
@app.route('/v0.1/tty/<tty_id>',  methods=['DELETE'])
@requires_auth
def delete_task(tty_id):
    try:
        tty = TTY.objects(id=tty_id).first()
    except:
        abort(404)
    if tty is None:
        abort(404)

    if not tty.dry_run:
        image_id = tty.uri # tty-uu3js81.it-dojo.io
        image_id = image_id[4:image_id.index(".")] # uu3js81
        output   = tty_controller("delete", tty.template, image_id).splitlines()

    tty.delete()
    return jsonify({'result': True})

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

def format_reply(tty):
    formatted_tty = {}
    for field in tty:
        if field == 'id':
            #replace id field for a control uri
            formatted_tty['endpoint'] = url_for('get_tty', tty_id=tty['id'], _external=True)
        elif field == 'created':
            formatted_tty['created'] = tty['created'].__str__()
        elif field == 'destroyed':
            formatted_tty['destroyed'] = tty['created'].__str__()
        else:
            formatted_tty[field] = tty[field]
    return formatted_tty
