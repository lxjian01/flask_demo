import os
from config import config

env = os.getenv("FLASK_DEMO", "default")

# create app
from app import create_app
app = create_app(config[env])

# 注册蓝图
from app.urls import register_app
register_app(app)

# make celery
from app import make_celery
celery = make_celery(app)

if __name__ == '__main__':
    app.run()


