"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests verify signup functionality including valid signups and error cases.
"""

import pytest


class TestActivitySignup:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_student_returns_200(self, client):
        """
        Test: Valid signup returns 200 OK and success message.
        
        Arrange: Client ready, Tennis Club has empty participants
        Act: Sign up new student (test@example.com) for Tennis Club
        Assert: Status is 200 and response contains success message
        """
        # Act
        response = client.post("/activities/Tennis Club/signup?email=test@example.com")
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "test@example.com" in response.json()["message"]

    def test_signup_adds_student_to_activity(self, client):
        """
        Test: Student is added to activity participants list.
        
        Arrange: Client ready, Tennis Club initially empty
        Act: Sign up new student for Tennis Club
        Assert: GET /activities shows student in Tennis Club participants
        """
        # Arrange
        student_email = "newstudent@example.com"
        
        # Act
        client.post(f"/activities/Tennis Club/signup?email={student_email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert student_email in activities["Tennis Club"]["participants"]

    def test_signup_invalid_activity_returns_404(self, client):
        """
        Test: Signup to non-existent activity returns 404 Not Found.
        
        Arrange: Client ready, "Fake Activity" does not exist
        Act: Attempt to sign up for non-existent activity
        Assert: Status is 404 with appropriate error detail
        """
        # Act
        response = client.post("/activities/Fake Activity/signup?email=test@example.com")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student_returns_400(self, client):
        """
        Test: Duplicate signup returns 400 Bad Request.
        
        Arrange: Student already signed up for Chess Club
        Act: Attempt to sign up same student for Chess Club again
        Assert: Status is 400 with duplicate signup error
        """
        # Arrange
        existing_student = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(f"/activities/Chess Club/signup?email={existing_student}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_multiple_students_different_activities(self, client):
        """
        Test: Multiple students can sign up for different activities.
        
        Arrange: Client ready
        Act: Sign up student1 for Tennis Club, student2 for Art Studio
        Assert: Both students appear in their respective activities
        """
        # Arrange
        student1 = "student1@example.com"
        student2 = "student2@example.com"
        
        # Act
        client.post(f"/activities/Tennis Club/signup?email={student1}")
        client.post(f"/activities/Art Studio/signup?email={student2}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert student1 in activities["Tennis Club"]["participants"]
        assert student2 in activities["Art Studio"]["participants"]
        assert student1 not in activities["Art Studio"]["participants"]
        assert student2 not in activities["Tennis Club"]["participants"]

    def test_signup_same_student_different_activities(self, client):
        """
        Test: Same student can sign up for different activities.
        
        Arrange: Client ready
        Act: Sign up same student for Tennis Club and Art Studio
        Assert: Student appears in both activities
        """
        # Arrange
        student_email = "multi@example.com"
        
        # Act
        client.post(f"/activities/Tennis Club/signup?email={student_email}")
        client.post(f"/activities/Art Studio/signup?email={student_email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert student_email in activities["Tennis Club"]["participants"]
        assert student_email in activities["Art Studio"]["participants"]

    def test_signup_missing_email_parameter(self, client):
        """
        Test: Missing email parameter returns appropriate error.
        
        Arrange: Client ready
        Act: Call signup endpoint without email query parameter
        Assert: Request fails (missing required parameter)
        """
        # Act
        response = client.post("/activities/Tennis Club/signup")
        
        # Assert
        # Missing required query parameter returns 422 Unprocessable Entity
        assert response.status_code == 422

    def test_signup_empty_email(self, client):
        """
        Test: Empty email string can be used (no validation in current implementation).
        
        Arrange: Client ready
        Act: Attempt signup with empty email string
        Assert: Request succeeds (current implementation allows empty strings)
        """
        # Act
        response = client.post("/activities/Tennis Club/signup?email=")
        
        # Assert
        # Current implementation accepts empty email (no validation)
        assert response.status_code == 200

    def test_signup_response_message_contains_details(self, client):
        """
        Test: Signup response includes student email and activity name.
        
        Arrange: Client ready
        Act: Sign up student for activity
        Assert: Response message contains both email and activity name
        """
        # Arrange
        student_email = "verify@example.com"
        activity_name = "Tennis Club"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={student_email}")
        message = response.json()["message"]
        
        # Assert
        assert student_email in message
        assert activity_name in message
