#!/usr/bin/env python3
import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the backend URL
BACKEND_URL = "https://dcebb859-d3a0-4791-bac5-696ddf89516c.preview.emergentagent.com/api"

def test_authentication():
    """Test the authentication flow: create user, login, verify session, logout"""
    logger.info("Testing Authentication Flow...")
    
    # 1. Create a test user
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass123",
        "role": "User"
    }
    
    logger.info("Step 1: Creating test user...")
    response = requests.post(f"{BACKEND_URL}/users", json=user_data)
    if response.status_code == 400 and "Username already exists" in response.json().get("detail", ""):
        logger.info("User already exists, continuing with login test")
    else:
        assert response.status_code == 200, f"Failed to create user: {response.text}"
        user = response.json()
        logger.info(f"Created user: {user['username']} with ID: {user['id']}")
        
        # Verify password_hash is stored
        assert "password_hash" in user, "Password hash not stored in user object"
        assert "password" not in user, "Plain password should not be stored"
    
    # 2. Login with the created user
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    logger.info("Step 2: Logging in with test user...")
    response = requests.post(f"{BACKEND_URL}/auth/login", json=login_data)
    assert response.status_code == 200, f"Failed to login: {response.text}"
    login_result = response.json()
    
    # Verify login response
    assert "session_token" in login_result, "Session token not returned in login response"
    assert login_result["username"] == "testuser", "Username mismatch in login response"
    
    session_token = login_result["session_token"]
    logger.info(f"Login successful, received session token: {session_token[:10]}...")
    
    # 3. Verify session
    logger.info("Step 3: Verifying session...")
    response = requests.get(f"{BACKEND_URL}/auth/verify?session_token={session_token}")
    assert response.status_code == 200, f"Failed to verify session: {response.text}"
    verify_result = response.json()
    
    # Verify session verification response
    assert verify_result["username"] == "testuser", "Username mismatch in session verification"
    assert "user_id" in verify_result, "User ID not returned in session verification"
    assert "role" in verify_result, "Role not returned in session verification"
    logger.info("Session verification successful")
    
    # 4. Logout
    logger.info("Step 4: Logging out...")
    response = requests.post(f"{BACKEND_URL}/auth/logout?session_token={session_token}")
    assert response.status_code == 200, f"Failed to logout: {response.text}"
    logout_result = response.json()
    
    # Verify logout response
    assert "message" in logout_result, "Logout message not returned"
    assert "successfully" in logout_result["message"].lower(), "Logout not successful"
    logger.info("Logout successful")
    
    # 5. Verify session is invalidated
    logger.info("Step 5: Verifying session is invalidated...")
    response = requests.get(f"{BACKEND_URL}/auth/verify?session_token={session_token}")
    assert response.status_code == 401, "Session should be invalidated after logout"
    logger.info("Session invalidation verified")
    
    logger.info("Authentication flow test completed successfully!")

if __name__ == "__main__":
    test_authentication()