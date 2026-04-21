"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.

Tests verify participant removal functionality including valid deletions and error cases.
"""

import pytest


class TestParticipantManagement:
    """Test suite for the DELETE /activities/{activity_name}/participants endpoint."""

    def test_delete_participant_returns_200(self, client):
        """
        Test: Deleting a participant returns 200 OK.
        
        Arrange: Client ready, student is in activity
        Act: Delete existing participant
        Assert: Status is 200 and response contains success message
        """
        # Arrange
        participant = "michael@mergington.edu"  # In Chess Club
        
        # Act
        response = client.delete(
            f"/activities/Chess Club/participants?email={participant}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_delete_removes_participant_from_activity(self, client):
        """
        Test: Participant is removed from activity list after deletion.
        
        Arrange: Client ready, participant is in activity
        Act: Delete participant, then fetch activities
        Assert: Participant no longer in activity
        """
        # Arrange
        participant = "michael@mergington.edu"
        
        # Act
        client.delete(f"/activities/Chess Club/participants?email={participant}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert participant not in activities["Chess Club"]["participants"]

    def test_delete_invalid_activity_returns_404(self, client):
        """
        Test: Deleting from non-existent activity returns 404.
        
        Arrange: Client ready
        Act: Attempt to delete participant from non-existent activity
        Assert: Status is 404 with appropriate error
        """
        # Act
        response = client.delete(
            "/activities/Fake Activity/participants?email=test@example.com"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_delete_nonexistent_participant_returns_404(self, client):
        """
        Test: Deleting non-existent participant returns 404.
        
        Arrange: Client ready, participant not in activity
        Act: Attempt to delete student not in activity
        Assert: Status is 404 with error message
        """
        # Act
        response = client.delete(
            "/activities/Tennis Club/participants?email=notinactivity@example.com"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not signed up" in response.json()["detail"]

    def test_delete_response_contains_details(self, client):
        """
        Test: Delete response includes participant email and activity name.
        
        Arrange: Client ready
        Act: Delete participant from activity
        Assert: Response message contains email and activity name
        """
        # Arrange
        participant = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants?email={participant}"
        )
        message = response.json()["message"]
        
        # Assert
        assert participant in message
        assert activity_name in message

    def test_delete_only_removes_from_specified_activity(self, client):
        """
        Test: Deleting participant only removes from specified activity, not others.
        
        Arrange: Client ready, sign up same student for multiple activities
        Act: Sign up student for two activities, delete from first activity
        Assert: Student removed from first activity but remains in second
        """
        # Arrange
        student = "multiaccess@example.com"
        
        # Sign up for two activities
        client.post(f"/activities/Tennis Club/signup?email={student}")
        client.post(f"/activities/Art Studio/signup?email={student}")
        
        # Act
        client.delete(f"/activities/Tennis Club/participants?email={student}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert student not in activities["Tennis Club"]["participants"]
        assert student in activities["Art Studio"]["participants"]

    def test_delete_multiple_participants_sequentially(self, client):
        """
        Test: Multiple participants can be deleted from same activity.
        
        Arrange: Client ready, multiple participants in activity
        Act: Delete multiple participants one by one
        Assert: All deleted participants removed from activity
        """
        # Arrange
        participant1 = "michael@mergington.edu"
        participant2 = "daniel@mergington.edu"
        
        # Act
        client.delete(f"/activities/Chess Club/participants?email={participant1}")
        client.delete(f"/activities/Chess Club/participants?email={participant2}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert participant1 not in activities["Chess Club"]["participants"]
        assert participant2 not in activities["Chess Club"]["participants"]

    def test_delete_from_empty_activity(self, client):
        """
        Test: Attempting to delete from activity with no participants returns 404.
        
        Arrange: Client ready, Tennis Club initially has no participants
        Act: Attempt to delete from empty activity
        Assert: Status is 404
        """
        # Act
        response = client.delete(
            "/activities/Tennis Club/participants?email=anyone@example.com"
        )
        
        # Assert
        assert response.status_code == 404

    def test_delete_missing_email_parameter(self, client):
        """
        Test: Missing email parameter returns appropriate error.
        
        Arrange: Client ready
        Act: Call delete endpoint without email query parameter
        Assert: Request fails (missing required parameter)
        """
        # Act
        response = client.delete("/activities/Chess Club/participants")
        
        # Assert
        # Missing required query parameter returns 422 Unprocessable Entity
        assert response.status_code == 422

    def test_delete_empty_email(self, client):
        """
        Test: Empty email string is handled by endpoint.
        
        Arrange: Client ready
        Act: Attempt delete with empty email string
        Assert: Returns 404 (email not found in any activity)
        """
        # Act
        response = client.delete(
            "/activities/Chess Club/participants?email="
        )
        
        # Assert
        assert response.status_code == 404
