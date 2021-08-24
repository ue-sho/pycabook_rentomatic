import pytest


from application.app import create_app


# conftest.pyというファイルにフィクスチャを記述すると、
# そのフィクスチャは複数のテストコードから呼び出すことが出来るようになります。
# テストの前処理
# pytest-flaskによって appは、client, config, live_serverなどの引数を受け取れるようになる
@pytest.fixture
def app():
    app = create_app("testing")

    return app