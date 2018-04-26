from api import app
from api.models import TTY
from api.decorators import async

from base64 import b64encode
from sh import tty_controller

@async
def async_tty_pool(app, template, required_instances):
    with app.app_context():
        available_free_instances = TTY.objects(template=template, active=False, dry_run=False).count()

        if available_free_instances < required_instances:
            required_instances = required_instances - available_free_instances
        else:
            required_instances  = 0

        for instance in range(required_instances):
            stdout  = {}
            for line in tty_controller("create", template + "/docker-compose.yml").splitlines():
                if line.find(':') >= 0:
                    k,v = line.split(":",2) # split at first : produce max 2 items
                else:
                    k,v = ['stdout', line]  # split at first : produce max 2 items
                stdout.setdefault(k.strip(), v.strip())  # add to dict & split at . into list

            uri    = stdout["uri"]
            readme = stdout["readme"]
            f      = open(readme, "r")
            readme = b64encode(f.read().encode('utf-8'))

            new_tty = TTY(
                        template = template,
                        username = "inactive@it-dojo.io",
                        uri      = uri,
                        readme   = readme,
                        active   = False,
                        dry_run  = False,
                      ).save()

def tty_pool(template, instances):
    async_tty_pool(app, template, instances)
