from api import db
from datetime import datetime

class TTY(db.Document):
    template   = db.StringField(required=True)
    username   = db.StringField(required=True)
    subdomain  = db.StringField(required=True, unique=True)
    created    = db.DateTimeField(default=datetime.now)
    destroyed  = db.DateTimeField()
    ttl        = db.IntField(604800) #7 days
    active     = db.BooleanField(default=True)
