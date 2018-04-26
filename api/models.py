from api import db
from datetime import datetime

class TTY(db.Document):
    template   = db.StringField(required=True)
    username   = db.StringField(required=True)
    uri        = db.StringField(required=True, unique=True)
    readme     = db.StringField(required=True)
    created    = db.DateTimeField(default=datetime.now)
    destroyed  = db.DateTimeField()
    ttl        = db.IntField(default=604800) #7 days
    active     = db.BooleanField(default=True)
    dry_run    = db.BooleanField(default=False)
