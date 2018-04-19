import os
import urllib.parse

class Config(object):
    #general settings
    APP_ADMINS = os.environ.get('APP_ADMINS') or 'admin@it-dojo.com'
    APP_ADMINS = APP_ADMINS.split()
    APP_FROM   = os.environ.get('APP_FROM')   or 'no-reply@it-dojo.io'

    #flask-mongoengine
    MONGODB_HOST     = os.environ.get('MONGODB_HOST')     or 'mongodb'
    MONGODB_TCP_PORT = os.environ.get('MONGODB_TCP_PORT') or 27017
    MONGODB_TCP_PORT = int(MONGODB_TCP_PORT)
    MONGODB_DB       = os.environ.get('MONGODB_DB')       or 'it-dojo-backend-api'
    MONGODB_USER     = os.environ.get('MONGODB_USER')     or 'it-dojo-backend-api'
    MONGODB_PASSWD   = os.environ.get('MONGODB_PASSWD')   or 'it-dojo-backend-api'

    MONGODB_USER     = urllib.parse.quote_plus(MONGODB_USER)
    MONGODB_PASSWD   = urllib.parse.quote_plus(MONGODB_PASSWD)

    MONGODB_SETTINGS = {
        'db':       MONGODB_DB,
        'host':     MONGODB_HOST,
        'port':     MONGODB_TCP_PORT,
        'username': MONGODB_USER,
        'password': MONGODB_PASSWD,
    }

    #mailgun
    MAILGUN_API    = os.environ.get('MAILGUN_API')    or 'you-will-never-guess'
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN') or 'domain.tld'
