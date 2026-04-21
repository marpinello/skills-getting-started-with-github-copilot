"""
Pytest configuration and shared fixtures for API tests.

Provides TestClient instance and state reset functionality for test isolation.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def reset_activities():
    """
    Fixture to reset the in-memory activities database before each test.
    
    This ensures test isolation by providing a clean state with default activities.
    """
    # Reset to initial state
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn and play tennis with other students",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": []
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and regional tournaments",
            "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Wednesdays and Saturdays, 2:00 PM - 4:00 PM",
            "max_participants": 25,
            "participants": ["natalie@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore various art mediums and techniques including painting, drawing, and sculpture",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM; Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Debate Club": {
            "description": "Develop public speaking and argumentation skills through competitive debate",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["james@mergington.edu", "grace@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science competitions and work on scientific research projects",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["rachel@mergington.edu"]
        }
    })
    yield
    # Cleanup happens automatically after test


@pytest.fixture
def client(reset_activities):
    """
    Fixture providing a TestClient instance for API testing.
    
    Automatically resets activities state before each test.
    """
    return TestClient(app)
