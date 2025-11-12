"""
Tests for user management
"""
import pytest
from fastapi import status


class TestUserManagement:
    """Test admin user management functionality"""

    def test_admin_can_list_users(self, client, admin_token, test_user):
        """Test admin can view all users"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 2  # At least admin and test_user

        usernames = [u["username"] for u in users]
        assert "admin" in usernames
        assert "testuser" in usernames

    def test_user_cannot_list_users(self, client, user_token):
        """Test regular user cannot view user list"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_user(self, client, admin_token, test_user):
        """Test admin can delete users"""
        response = client.delete(
            f"/api/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify user is deleted
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        users = response.json()
        user_ids = [u["id"] for u in users]
        assert test_user.id not in user_ids

    def test_admin_cannot_delete_self(self, client, admin_token, admin_user):
        """Test admin cannot delete their own account"""
        response = client.delete(
            f"/api/admin/users/{admin_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "own account" in response.json()["detail"].lower()

    def test_delete_nonexistent_user(self, client, admin_token):
        """Test deleting non-existent user"""
        response = client.delete(
            "/api/admin/users/99999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_cannot_delete_users(self, client, user_token, admin_user):
        """Test regular user cannot delete users"""
        response = client.delete(
            f"/api/admin/users/{admin_user.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_users_list_includes_role(self, client, admin_token):
        """Test that user list includes role information"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        users = response.json()

        for user in users:
            assert "role" in user
            assert user["role"] in ["user", "admin"]

    def test_users_list_does_not_expose_passwords(self, client, admin_token):
        """Test that user list doesn't expose password hashes"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        users = response.json()

        for user in users:
            assert "password" not in user
            assert "hashed_password" not in user


class TestUserRoles:
    """Test user role assignment and enforcement"""

    def test_new_user_gets_user_role(self, client):
        """Test new signups get USER role by default"""
        response = client.post(
            "/api/auth/signup",
            json={"username": "newuser", "password": "password123"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["role"] == "user"

    def test_admin_role_enforced_on_upload(self, client, user_token):
        """Test USER role cannot upload files"""
        csv_content = b"name,age\nJohn,25\n"
        files = {"file": ("test.csv", csv_content, "text/csv")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_role_enforced_on_user_management(self, client, user_token):
        """Test USER role cannot manage users"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN