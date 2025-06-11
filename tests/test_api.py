import pytest
from fastapi.testclient import TestClient
import shutil
import os
import json

from main import app
from app.routers.users import set_user_repository
from app.repositories.user_repository import UserRepository
from app.config import settings

@pytest.fixture(autouse=True) # Run before and after each test
def setup_and_teardown():

    source_test_json_file = "tests/test_users.json"
    temp_test_json_file = "test.json"
    
    # Copy our test data file to a temporary file.
    shutil.copy(source_test_json_file, temp_test_json_file)

    # Point the app's settings to our temporary database file.
    original_json_setting = settings.USERS_FILE
    settings.USERS_FILE = temp_test_json_file
    
    # Create a fresh repository instance for the test.
    test_repository = UserRepository()
    set_user_repository(test_repository)
    
    yield
    
    # Clean up the temporary file after the test is done.
    os.remove(temp_test_json_file)
    settings.USERS_FILE = original_json_setting

# Create a client to make requests to our app
client = TestClient(app)

def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    usernames = response.json()
    assert isinstance(usernames, list)
    assert "John Doe" in usernames
    assert "Jane Smith" in usernames

def test_create_user_success():
    new_user_data = {
      "id": "333333333",
      "name": "Test User",
      "phone": "053-3333333",
      "address": "1 Test Lane, Testville"
    }
    
    response = client.post("/users/", json=new_user_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"
    
    # Verify the data was actually saved by reading the test file
    with open(settings.USERS_FILE, "r") as f:
        data = json.load(f)
        assert len(data) == 3
        assert any(user["id"] == "333333333" for user in data)

def test_create_user_fails_on_duplicate_id():
    duplicate_user_data = {
      "id": "111111111", # This ID exists in test_users.json
      "name": "Another John",
      "phone": "051-1111111",
      "address": "Another Address"
    }
    
    response = client.post("/users/", json=duplicate_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with ID 111111111 already exists" 