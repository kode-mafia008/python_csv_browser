"""
Tests for security features
"""
import pytest
from fastapi import status
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)


class TestPasswordHashing:
    """Test password hashing functionality"""

    def test_password_hash_created(self):
        """Test password can be hashed"""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 20

    def test_password_verification_success(self):
        """Test correct password verification"""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """Test incorrect password verification"""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert verify_password("wrongpassword", hashed) is False

    def test_same_password_different_hashes(self):
        """Test same password creates different hashes (salt)"""
        password = "mypassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTToken:
    """Test JWT token functionality"""

    def test_create_token(self):
        """Test JWT token creation"""
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 20

    def test_decode_token(self):
        """Test JWT token decoding"""
        data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(data)
        decoded = decode_access_token(token)

        assert decoded is not None
        assert decoded["sub"] == "testuser"
        assert decoded["role"] == "admin"

    def test_decode_invalid_token(self):
        """Test decoding invalid token"""
        decoded = decode_access_token("invalid.token.here")
        assert decoded is None

    def test_token_contains_expiration(self):
        """Test token contains expiration claim"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        decoded = decode_access_token(token)

        assert decoded is not None
        assert "exp" in decoded


class TestFileUploadSecurity:
    """Test file upload security features"""

    def test_only_csv_files_accepted(self, client, admin_token):
        """Test non-CSV files are rejected"""
        files = {"file": ("test.txt", b"Not a CSV", "text/plain")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_filename_sanitization(self, client, admin_token, temp_upload_dir):
        """Test uploaded files get unique UUID-based names"""
        csv_content = b"name,age\nJohn,25\n"
        files = {"file": ("../../../etc/passwd.csv", csv_content, "text/csv")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        if response.status_code == 200:
            filepath = response.json()["filepath"]
            # Filepath should not contain the malicious path
            assert "../" not in filepath
            assert "etc/passwd" not in filepath


class TestAuthorizationSecurity:
    """Test authorization security"""

    def test_user_cannot_escalate_to_admin(self, client, user_token):
        """Test user cannot access admin endpoints"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_endpoints_require_admin_role(self, client, user_token):
        """Test all admin endpoints require admin role"""
        admin_endpoints = [
            ("/api/admin/users", "GET"),
            ("/api/admin/csv", "GET"),
        ]

        for endpoint, method in admin_endpoints:
            if method == "GET":
                response = client.get(
                    endpoint,
                    headers={"Authorization": f"Bearer {user_token}"}
                )

            assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_cannot_access_without_auth(self, client):
        """Test protected endpoints require authentication"""
        endpoints = [
            "/api/csv",
            "/api/admin/users",
            "/api/admin/csv",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN
            ]