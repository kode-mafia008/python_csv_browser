"""
Tests for CSV file operations
"""
import pytest
import os
from fastapi import status
from io import BytesIO


class TestCSVUpload:
    """Test CSV file upload functionality"""

    def test_upload_csv_success(self, client, admin_token, temp_upload_dir):
        """Test successful CSV upload"""
        csv_content = b"name,age,city\nJohn,25,NYC\nJane,30,LA\n"
        files = {"file": ("users.csv", csv_content, "text/csv")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["filename"] == "users.csv"
        assert data["size"] == len(csv_content)
        assert "id" in data
        assert "upload_date" in data
        assert os.path.exists(data["filepath"])

    def test_upload_non_csv_file(self, client, admin_token, temp_upload_dir):
        """Test upload of non-CSV file is rejected"""
        files = {"file": ("test.txt", b"Not a CSV", "text/plain")}

        response = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "csv" in response.json()["detail"].lower()

    def test_upload_without_file(self, client, admin_token):
        """Test upload without file"""
        response = client.post(
            "/api/admin/csv/upload",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_upload_creates_unique_filename(self, client, admin_token, temp_upload_dir):
        """Test that uploaded files get unique names"""
        csv_content = b"name,age\nJohn,25\n"
        files = {"file": ("same.csv", csv_content, "text/csv")}

        # Upload same file twice
        response1 = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        files = {"file": ("same.csv", csv_content, "text/csv")}
        response2 = client.post(
            "/api/admin/csv/upload",
            files=files,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK

        # Filepaths should be different (UUID-based)
        filepath1 = response1.json()["filepath"]
        filepath2 = response2.json()["filepath"]
        assert filepath1 != filepath2


class TestCSVList:
    """Test CSV file listing"""

    def test_list_csv_files_empty(self, client, user_token):
        """Test listing when no files exist"""
        response = client.get(
            "/api/csv",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_csv_files_with_files(self, client, user_token, sample_csv_file):
        """Test listing CSV files"""
        response = client.get(
            "/api/csv",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["filename"] == "sample.csv"
        assert data[0]["id"] == sample_csv_file.id

    def test_list_requires_authentication(self, client):
        """Test that listing requires authentication"""
        response = client.get("/api/csv")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCSVView:
    """Test CSV file viewing"""

    def test_view_csv_content(self, client, user_token, sample_csv_file):
        """Test viewing CSV content as JSON"""
        response = client.get(
            f"/api/csv/{sample_csv_file.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "columns" in data
        assert "data" in data
        assert "row_count" in data
        assert data["columns"] == ["name", "age", "city"]
        assert len(data["data"]) == 2
        assert data["row_count"] == 2

    def test_view_nonexistent_csv(self, client, user_token):
        """Test viewing non-existent CSV"""
        response = client.get(
            "/api/csv/99999",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_view_requires_authentication(self, client, sample_csv_file):
        """Test that viewing requires authentication"""
        response = client.get(f"/api/csv/{sample_csv_file.id}")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestCSVDownload:
    """Test CSV file download"""

    def test_download_csv_file(self, client, user_token, sample_csv_file):
        """Test downloading CSV file"""
        response = client.get(
            f"/api/csv/{sample_csv_file.id}/download",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/csv"
        assert "content-disposition" in response.headers
        assert "sample.csv" in response.headers["content-disposition"]
        assert b"name,age,city" in response.content

    def test_download_nonexistent_csv(self, client, user_token):
        """Test downloading non-existent CSV"""
        response = client.get(
            "/api/csv/99999/download",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCSVDelete:
    """Test CSV file deletion"""

    def test_delete_csv_success(self, client, admin_token, sample_csv_file):
        """Test successful CSV deletion"""
        filepath = sample_csv_file.filepath

        response = client.delete(
            f"/api/admin/csv/{sample_csv_file.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify file is deleted from disk
        assert not os.path.exists(filepath)

        # Verify cannot view deleted file
        response = client.get(
            f"/api/csv/{sample_csv_file.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_csv(self, client, admin_token):
        """Test deleting non-existent CSV"""
        response = client.delete(
            "/api/admin/csv/99999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_requires_admin(self, client, user_token, sample_csv_file):
        """Test that deletion requires admin role"""
        response = client.delete(
            f"/api/admin/csv/{sample_csv_file.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN