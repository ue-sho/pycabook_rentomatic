from flask import Flask

from application.rest import room


def create_app(config_name):

    # __name__ == application.app
    # このクラスのインスタンスは、WSGIアプリケーションになる
    # WSGI = Web Server Gateway Interface
    # WebサーバとWebアプリケーションを接続するための、標準化されたインタフェース定義
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    # config設定により、いろいろ設定が出来る
    # https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/config.html
    app.config.from_object(config_module)
	
    # blueprint = Blueprint("room", __name__)
    # room という名前で、appplication.rest.room モジュールを登録している
    app.register_blueprint(room.blueprint)
	
    return app