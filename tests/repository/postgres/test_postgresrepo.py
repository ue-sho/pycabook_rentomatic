import pytest

# これでpytest -svv -m integration
# そのラベルでマークされたテストのみを実行するようにpytestに要求するために実行できます。
# pytest.ini に定義がある
pytestmark = pytest.mark.integration


def test_dummy():
    pass