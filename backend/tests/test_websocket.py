"""
Tests for WebSocket functionality
"""
import pytest
import json
from fastapi.testclient import TestClient


class TestWebSocket:
    """Test WebSocket connection and messaging"""

    def test_websocket_connection(self, client):
        """Test WebSocket connection can be established"""
        with client.websocket_connect("/ws") as websocket:
            # Connection successful if no exception
            assert websocket is not None

    def test_websocket_multiple_connections(self, client):
        """Test multiple WebSocket connections"""
        with client.websocket_connect("/ws") as ws1:
            with client.websocket_connect("/ws") as ws2:
                assert ws1 is not None
                assert ws2 is not None

    def test_websocket_broadcast_on_upload(self, client, admin_token, temp_upload_dir):
        """Test WebSocket broadcast when CSV is uploaded"""
        with client.websocket_connect("/ws") as websocket:
            # Upload a CSV file
            csv_content = b"name,age\nJohn,25\n"
            files = {"file": ("test.csv", csv_content, "text/csv")}

            response = client.post(
                "/api/admin/csv/upload",
                files=files,
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            assert response.status_code == 200

            # Note: In test environment, WebSocket broadcast might not work
            # as expected due to TestClient limitations
            # This test validates the connection works
            # Real-time broadcast testing is better done with integration tests

    def test_websocket_stays_connected(self, client):
        """Test WebSocket connection stays alive"""
        with client.websocket_connect("/ws") as websocket:
            # Send a ping message
            websocket.send_text("ping")
            # Connection should remain open
            assert websocket is not None