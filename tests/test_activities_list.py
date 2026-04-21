"""
Tests for the GET /activities endpoint.

Tests verify responses for listing all extracurricular activities.
"""

import pytest


class TestActivitiesList:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """
        Test: GET /activities returns 200 OK status.
        
        Arrange: Client ready
        Act: Call GET /activities
        Assert: Status code is 200
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """
        Test: GET /activities returns all 9 activities.
        
        Arrange: Client ready
        Act: Call GET /activities and get response JSON
        Assert: Response contains exactly 9 activity names
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert len(activities_data) == 9
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data
        assert "Gym Class" in activities_data
        assert "Tennis Club" in activities_data
        assert "Basketball Team" in activities_data
        assert "Drama Club" in activities_data
        assert "Art Studio" in activities_data
        assert "Debate Club" in activities_data
        assert "Science Olympiad" in activities_data

    def test_activity_has_required_fields(self, client):
        """
        Test: Each activity has all required fields.
        
        Arrange: Client ready
        Act: Call GET /activities and get response data
        Assert: Each activity contains description, schedule, max_participants, and participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info, dict), f"{activity_name} is not a dictionary"
            assert required_fields.issubset(activity_info.keys()), \
                f"{activity_name} missing required fields"

    def test_activity_participants_is_list(self, client):
        """
        Test: Participants field is always a list.
        
        Arrange: Client ready
        Act: Call GET /activities
        Assert: Participants field is a list for all activities
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["participants"], list), \
                f"{activity_name} participants is not a list"

    def test_activity_max_participants_is_integer(self, client):
        """
        Test: max_participants field is an integer.
        
        Arrange: Client ready
        Act: Call GET /activities
        Assert: max_participants is an integer for all activities
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["max_participants"], int), \
                f"{activity_name} max_participants is not an integer"

    def test_activities_response_is_json_dict(self, client):
        """
        Test: Response is a JSON dictionary/object.
        
        Arrange: Client ready
        Act: Call GET /activities
        Assert: Response is a dictionary
        """
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert isinstance(activities_data, dict), "Response is not a JSON object"
