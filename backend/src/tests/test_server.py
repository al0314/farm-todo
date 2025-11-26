# tests/test_server.py
from datetime import datetime
from fastapi import status
from server import NewList, NewListResponse, ToDoItemUpdate


def test_get_all_lists(client):
    """Test getting all lists."""
    response = client.get("/api/lists")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # We mocked one list
    assert data[0]["id"] == "1"
    assert data[0]["name"] == "Test List"


def test_create_todo_list(client):
    """Test creating a new to-do list."""
    new_list = {"name": "My New List"}
    response = client.post("/api/lists", json=new_list)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == "new-list-id"
    assert data["name"] == new_list["name"]


def test_get_todo_list(client):
    """Test getting a specific to-do list."""
    response = client.get("/api/lists/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1"
    assert data["name"] == "Test List"


def test_delete_todo_list(client):
    """Test deleting a to-do list."""
    response = client.delete("/api/lists/1")
    assert response.status_code == 200
    data = response.json()
    assert data is True  # Mocked to return True on delete


def test_create_item(client):
    """Test creating an item in a to-do list."""
    new_item = {"label": "New Task"}
    response = client.post("/api/lists/1/items/", json=new_item)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["label"] == "New Task"


def test_delete_item(client):
    """Test deleting an item from a to-do list."""
    response = client.delete("/api/lists/1/items/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0  # We mocked the item list to be empty


def test_set_checked_state(client):
    """Test setting the checked state of an item."""
    update = ToDoItemUpdate(item_id="1", checked_state=True)
    response = client.patch("/api/lists/1/checked_state", json=update.dict())
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["checked"] is True
