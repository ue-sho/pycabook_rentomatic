import pytest

from rentomatic.repository.postgres_objects import Room

# これでpytest -svv -m integration
# そのラベルでマークされたテストのみを実行するようにpytestに要求するために実行できます。
# pytest.ini に定義がある
pytestmark = pytest.mark.integration


def test_dummy(pg_session):
    assert len(pg_session.query(Room).all()) == 4