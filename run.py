import os
from app.config import config

env = os.getenv("FLASK_DEMO", "default")

# create app
from app import create_app
app = create_app(config[env])

# create celery
from app import make_celery
celery = make_celery(app)

if __name__ == '__main__':
    app.run(port=8080)


