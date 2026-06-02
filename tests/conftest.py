import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Create a TestClient instance for testing."""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """
    Reset activities to initial state for each test.
    Returns a deep copy so modifications don't affect other tests.
    """
    # Save original activities state
    original = copy.deepcopy(activities)
    
    # Yield to test
    yield activities
    
    # Restore original state after test
    activities.clear()
    activities.update(original)
