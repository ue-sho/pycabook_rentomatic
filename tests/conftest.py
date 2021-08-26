import pytest

from application.app import create_app
from manage import read_json_configuration


# conftest.pyというファイルにフィクスチャを記述すると、
# そのフィクスチャは複数のテストコードから呼び出すことが出来るようになります。
# テストの前処理
# pytest-flaskによって appは、client, config, live_serverなどの引数を受け取れるようになる
@pytest.fixture
def app():
    app = create_app("testing")

    return app


# pytest -svv --integration とすると、setupで
def pytest_addoption(parser):
    parser.addoption(
        "--integration", action="store_true", help="run integration tests"
    )



# すべてのテストのpytestセットアップへのフックです。
# 変数itemにはテスト自体（実際には_pytest.python.Functionオブジェクト）が含まれ、
# テスト自体には2つの有用な情報が含まれています。
# 1つ目は属性item.keywordsで、テストマーク、テストの名前、ファイル、モジュール、
# テスト内で発生するパッチに関する情報など、他の多くの興味深いものが含まれています。
# 2つ目は、item.config解析されたpytestコマンドラインを含む属性です。
#
# したがって、テストがintegration（'integration' in item.keywords）でマークされていて、
# オプション--integrationが存在しない場合（not item.config.getvalue("integration")）、テストはスキップされます。
def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getvalue(
        "integration"
    ):
        pytest.skip("need --integration option to run")


@pytest.fixture(scope="session")
def app_configuration():
    return read_json_configuration("testing")