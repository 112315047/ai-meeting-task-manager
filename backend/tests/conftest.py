import os
import tempfile
import pytest
from backend.app import create_app
from backend.database import init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    # We need to ensure we use the test database we just created
    # Override the get_db behavior for tests if needed, or rely on env var
    os.environ['DATABASE_URL'] = db_path

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
