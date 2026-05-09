import pytest

from fastapi.testclient import TestClient

pytest_plugins = [
    "tests.fixtures.db_fixtures",
    "tests.fixtures.auth_fixtures",
    "tests.fixtures.url_fixtures",
]
