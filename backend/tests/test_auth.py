"""
Tests for authentication endpoints
"""
import pytest
from fastapi import status


class TestSignup:
    """Test user signup functionality"""

    def test_signup_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/signup",
            json={"username": "newuser", "password": "password123"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["role"] == "user"
        assert "id" in data
        assert "password" not in data

    def test_signup_duplicate_username(self, client, test_user):
        """Test signup with existing username"""
        response = client.post(
            "/api/auth/signup",
            json={"username": "testuser", "password": "password123"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()

    def test_signup_invalid_username(self, client):
        """Test signup with invalid username"""
        response = client.post(
            "/api/auth/signup",
            json={"username": "ab", "password": "password123"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_signup_invalid_password(self, client):
        """Test signup with short password"""
        response = client.post(
            "/api/auth/signup",
            json={"username": "newuser", "password": "12345"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_signup_default_role_is_user(self, client):
        """Test that new users get USER role by default"""
        response = client.post(
            "/api/auth/signup",
            json={"username": "regularuser", "password": "password123"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["role"] == "user"


class TestLogin:
    """Test user login functionality"""

    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_admin_success(self, client, admin_user):
        """Test admin login"""
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "adminpass123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            json={"username": "nonexistent", "password": "password123"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_credentials(self, client):
        """Test login without credentials"""
        response = client.post("/api/auth/login", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestJWTToken:
    """Test JWT token functionality"""

    def test_token_contains_role_claim(self, client, admin_user):
        """Test that JWT token includes role claim"""
        from app.core.security import decode_access_token

        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "adminpass123"}
        )
        token = response.json()["access_token"]
        payload = decode_access_token(token)

        assert payload is not None
        assert payload["sub"] == "admin"
        assert payload["role"] == "admin"

    def test_protected_route_without_token(self, client):
        """Test accessing protected route without token"""
        response = client.get("/api/csv")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_protected_route_with_invalid_token(self, client):
        """Test accessing protected route with invalid token"""
        response = client.get(
            "/api/csv",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_route_with_valid_token(self, client, user_token):
        """Test accessing protected route with valid token"""
        response = client.get(
            "/api/csv",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK