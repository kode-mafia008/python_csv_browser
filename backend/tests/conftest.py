"""
Test fixtures and configuration for pytest
"""
import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.csv_file import CSVFile


# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with overridden database dependency"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user with USER role"""
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpass123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_user(db):
    """Create a test admin user"""
    admin = User(
        username="admin",
        hashed_password=get_password_hash("adminpass123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def user_token(client, test_user):
    """Get JWT token for regular user"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def admin_token(client, admin_user):
    """Get JWT token for admin user"""
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "adminpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def temp_upload_dir():
    """Create a temporary directory for file uploads"""
    temp_dir = tempfile.mkdtemp()
    original_upload_dir = os.environ.get("UPLOAD_DIR")
    os.environ["UPLOAD_DIR"] = temp_dir
    yield temp_dir
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    if original_upload_dir:
        os.environ["UPLOAD_DIR"] = original_upload_dir
    else:
        os.environ.pop("UPLOAD_DIR", None)


@pytest.fixture(scope="function")
def sample_csv_file(db, admin_user, temp_upload_dir):
    """Create a sample CSV file in database and disk"""
    csv_content = "name,age,city\nJohn,25,NYC\nJane,30,LA\n"
    filepath = os.path.join(temp_upload_dir, "sample.csv")

    with open(filepath, "w") as f:
        f.write(csv_content)

    csv_file = CSVFile(
        filename="sample.csv",
        filepath=filepath,
        size=len(csv_content),
        uploader_id=admin_user.id
    )
    db.add(csv_file)
    db.commit()
    db.refresh(csv_file)
    return csv_file