import bjoern
from api import app

bjoern.run(
    wsgi_app=app,
    host='0.0.0.0',
    port=8000,
    reuse_port=True
)
