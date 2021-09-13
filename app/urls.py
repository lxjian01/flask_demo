from app.errors import error
from app.main import main
from app.views.auth.user import user


def register_app(app):
    # 注册蓝图main和error
    app.register_blueprint(error)
    app.register_blueprint(main)
    # auth
    app.register_blueprint(user)