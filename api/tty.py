from api import app
from api.models import TTY
from api.decorators import async

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
            output  = tty_controller("create", template + ".yml").splitlines()
            uri     = output[-1]

            new_tty = TTY(
                        template = template,
                        username = "inactive@it-dojo.io",
                        uri      = uri,
                        active   = False,
                        dry_run  = False,
                      ).save()

def tty_pool(template, instances):
    async_tty_pool(app, template, instances)
