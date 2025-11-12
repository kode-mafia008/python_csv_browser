"""
Tests for role-based authorization
"""
import pytest
from fastapi import status


class TestRoleBasedAccess:
    """Test role-based access control"""

    def test_user_can_access_csv_list(self, client, user_token):
        """Test that regular users can list CSVs"""
        response = client.get(
            "/api/csv",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_user_cannot_upload_csv(self, client, user_token):
        """Test that regular users cannot upload CSVs"""
        csv_content = b"name,age\nJohn,25\n"
        files = {"file": ("test.csv", csv_content, "text/csv")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "admin" in response.json()["detail"].lower()

    def test_user_cannot_delete_csv(self, client, user_token, sample_csv_file):
        """Test that regular users cannot delete CSVs"""
        response = client.delete(
            f"/api/admin/csv/{sample_csv_file.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_view_users(self, client, user_token):
        """Test that regular users cannot view user list"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_delete_users(self, client, user_token, admin_user):
        """Test that regular users cannot delete users"""
        response = client.delete(
            f"/api/admin/users/{admin_user.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_upload_csv(self, client, admin_token, temp_upload_dir):
        """Test that admin can upload CSVs"""
        csv_content = b"name,age\nJohn,25\n"
        files = {"file": ("test.csv", csv_content, "text/csv")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_csv(self, client, admin_token, sample_csv_file):
        """Test that admin can delete CSVs"""
        response = client.delete(
            f"/api/admin/csv/{sample_csv_file.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_can_view_users(self, client, admin_token):
        """Test that admin can view user list"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_admin_can_delete_users(self, client, admin_token, test_user):
        """Test that admin can delete users"""
        response = client.delete(
            f"/api/admin/users/{test_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestAdminSelfProtection:
    """Test admin self-protection features"""

    def test_admin_cannot_delete_self(self, client, admin_token, admin_user):
        """Test that admin cannot delete their own account"""
        response = client.delete(
            f"/api/admin/users/{admin_user.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "own account" in response.json()["detail"].lower()