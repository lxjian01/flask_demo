from app.errors import error
from app.views import main


def register_app(app):
    # 注册蓝图main和error
    app.register_blueprint(error)
    app.register_blueprint(main)
    # permission
