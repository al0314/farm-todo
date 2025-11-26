import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from server import app, ToDoDAL, ListSummary, ToDoList
import logging

logging.basicConfig(level=logging.DEBUG)

# Helper function to create a fake async generator for list_todo_lists
async def mock_list_todo_lists():
    """Fake async generator for list_todo_lists."""
    logging.debug("Inside mock_list_todo_lists generator")
    yield ListSummary(id="1", name="Test List", item_count=0)
    logging.debug("Mock list_todo_lists completed.")

# Helper function to mock create_item dynamically
async def mock_create_item(list_id, label):
    """Simulate creating a new ToDoList item with a given label."""
    return ToDoList(
        id="1",
        name="Test List",
        items=[{"id": "1", "label": label, "checked": False}]
    )


# Helper function to mock delete_item
async def mock_delete_item(doc_id, item_id):
    """Simulate deleting a ToDoList item."""
    return ToDoList(id=doc_id, name="Test List", items=[])


@pytest.fixture
def mock_dal():
    """Mock the ToDoDAL."""
    dal = MagicMock(ToDoDAL)
    
    # Mock list_todo_lists to return an async generator.
    # Assign the async generator function directly so calling dal.list_todo_lists() returns an async iterator
    dal.list_todo_lists = mock_list_todo_lists  # async generator function

    # Mock other methods with the appropriate side effects
    dal.create_item = AsyncMock(side_effect=mock_create_item)
    dal.delete_item = AsyncMock(side_effect=mock_delete_item)

    # Return fixed mock data for other methods
    dal.create_todo_list.return_value = "new-list-id"
    dal.get_todo_list.return_value = ToDoList(id="1", name="Test List", items=[])
    dal.delete_todo_list.return_value = True
    dal.set_checked_state.return_value = ToDoList(id="1", name="Test List", items=[{
        "id": "1", "label": "Test Item", "checked": True
    }])

    return dal


@pytest.fixture
def client(mock_dal):
    """Override the DAL dependency for the FastAPI app."""
    app.todo_dal = mock_dal
    return TestClient(app)


# Now, let's add a simple test to confirm if the generator works
@pytest.mark.asyncio
async def test_get_all_lists(client):
    """Test for '/api/lists' endpoint."""
    response = client.get("/api/lists")
    
    assert response.status_code == 200
    result = response.json()
    
    logging.debug(f"Response: {result}")
    assert len(result) == 2
    assert result[0]["name"] == "Test List"
    assert result[1]["name"] == "Another List"
