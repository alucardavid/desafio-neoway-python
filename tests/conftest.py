import pytest
from app.database.base import Base

@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base