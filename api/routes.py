from flask import render_template, flash, redirect, url_for, request, abort, jsonify

from api import app, bcrypt
from api.models import TTY
from api.decorators import requires_auth

from datetime import datetime

domain = app.config['APP_DOMAIN']

# temporal imports ==================================================================
from api import db
from random import randint
#====================================================================================

ttys = [
    {
        'id': 1,
        'subdomain': u'tty-11111',
        'template': u'tty-tmux',
        'username': u'test@it-dojo.io',
        'created': db.DateTimeField(default=datetime.now),
        'destroyed': db.DateTimeField(default=datetime.now),
        'ttl': 604800,
        'active': True,
    },
    {
        'id': 2,
        'subdomain': u'tty-22222',
        'template': u'tty-tmux',
        'username': u'foo@it-dojo.io',
        'created': db.DateTimeField(default=datetime.now),
        'destroyed': db.DateTimeField(default=datetime.now),
        'ttl': 604800,
        'active': True,
    },
    {
        'id': 3,
        'subdomain': u'tty-33333',
        'template': u'tty-tmux',
        'username': u'bar@it-dojo.io',
        'created': db.DateTimeField(default=datetime.now),
        'destroyed': db.DateTimeField(default=datetime.now),
        'ttl': 604800,
        'active': True,
    },
]
# ttys = []

#____________________________________________________[ INDEX ]
@app.route('/v0.1/tty/', methods=['GET'])
@app.route('/v0.1/tty', methods=['GET'])
@requires_auth
def get_ttys():
    # ttys = TTY.objects()
    return jsonify({'ttys': [format_reply(tty) for tty in ttys]})

@app.route('/v0.1/tty/<int:tty_id>/', methods=['GET'])
@app.route('/v0.1/tty/<int:tty_id>', methods=['GET'])
@requires_auth
def get_tty(tty_id):
    tty = [tty for tty in ttys if tty['id'] == tty_id]
    if len(tty) == 0:
        abort(404)
    return jsonify({'tty': format_reply(tty[0])})

@app.route('/v0.1/tty/', methods=['POST'])
@app.route('/v0.1/tty', methods=['POST'])
@requires_auth
def post_tty():
    if not request.json or not 'template' in request.json or not 'username' in request.json:
        abort(400)

    tty = {
        'id': ttys[-1]['id'] + 1,
        'template': request.json['template'],
        'username': request.json['username'],
        'subdomain': u'tty-' + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)),
        'created': db.DateTimeField(default=datetime.now),
        'destroyed': db.DateTimeField(default=datetime.now),
        'ttl': 604800,
        'active': True,
    }

    ttys.append(tty)
    return jsonify({'tty': format_reply(tty)}), 201

@app.route('/v0.1/tty/<int:tty_id>/', methods=['PUT'])
@app.route('/v0.1/tty/<int:tty_id>',  methods=['PUT'])
@requires_auth
def update_task(tty_id):
    tty = [tty for tty in ttys if tty['id'] == tty_id]
    if len(tty) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'template' in request.json and type(request.json['template']) != unicode:
        abort(400)
    if 'username' in request.json and type(request.json['username']) is not unicode:
        abort(400)
    if 'active' in request.json and type(request.json['active']) is not bool:
        abort(400)
    tty[0]['template'] = request.json.get('template', tty[0]['template'])
    tty[0]['username'] = request.json.get('username', tty[0]['username'])
    tty[0]['active'] = request.json.get('active', tty[0]['active'])
    return jsonify({'tty': format_reply(tty[0])})

@app.route('/v0.1/tty/<int:tty_id>/', methods=['DELETE'])
@app.route('/v0.1/tty/<int:tty_id>', methods=['DELETE'])
@requires_auth
def delete_task(tty_id):
    tty = [tty for tty in ttys if tty['id'] == tty_id]
    if len(tty) == 0:
        abort(404)
    ttys.remove(tty[0])
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

def format_reply(tty):
    new_tty = {}
    for field in tty:
        if field == 'id':
            #replace id field for a control uri
            new_tty['endpoint'] = url_for('get_tty', tty_id=tty['id'], _external=True)
        elif field == 'subdomain':
            new_tty['uri'] = tty['subdomain'] + '.' + domain
        elif field == 'created':
            new_tty['created'] = tty['created'].__str__()
        elif field == 'destroyed':
            new_tty['destroyed'] = tty['created'].__str__()
        else:
            new_tty[field] = tty[field]
    return new_tty
