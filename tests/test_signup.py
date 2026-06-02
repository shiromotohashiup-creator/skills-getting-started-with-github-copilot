import pytest


class TestSignup:
    """Test suite for /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_success(self, client, clean_activities):
        """
        Arrange: Initialize activities with known participants
        Act: Sign up a new student for an activity
        Assert: Verify status 200, message is correct, and participant is added
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "new_student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in clean_activities[activity_name]["participants"]

    def test_signup_multiple_students_success(self, client, clean_activities):
        """
        Arrange: Prepare multiple new email addresses
        Act: Sign up each student sequentially for the same activity
        Assert: Verify all are added correctly with status 200
        """
        # Arrange
        activity_name = "Programming Class"
        new_emails = [
            "alice@mergington.edu",
            "bob@mergington.edu",
            "charlie@mergington.edu"
        ]
        
        # Act & Assert
        for email in new_emails:
            response = client.post(
                f"/activities/{activity_name}/signup?email={email}",
                follow_redirects=True
            )
            assert response.status_code == 200
            assert email in clean_activities[activity_name]["participants"]
        
        # Final assertion: verify all 3 + existing 2 = 5 participants
        assert len(clean_activities[activity_name]["participants"]) == 5

    def test_signup_nonexistent_activity_404(self, client, clean_activities):
        """
        Arrange: Prepare a non-existent activity name
        Act: Attempt to sign up for that activity
        Assert: Verify status 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_duplicate_registration_400(self, client, clean_activities):
        """
        Arrange: Use an already registered student email from initial data
        Act: Attempt to sign up the same student again
        Assert: Verify status 400 with "Student already signed up" message
        """
        # Arrange
        activity_name = "Chess Club"
        # From initial data: "michael@mergington.edu" is already in Chess Club
        duplicate_email = "michael@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={duplicate_email}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up"
        # Verify participants count didn't change
        assert len(clean_activities[activity_name]["participants"]) == initial_count

    def test_signup_duplicate_after_new_signup_400(self, client, clean_activities):
        """
        Arrange: Sign up a new student once
        Act: Attempt to sign them up again for the same activity
        Assert: Verify status 400 on second attempt
        """
        # Arrange
        activity_name = "Gym Class"
        new_email = "duplicate_test@mergington.edu"
        
        # Sign up once (first signup)
        response1 = client.post(
            f"/activities/{activity_name}/signup?email={new_email}",
            follow_redirects=True
        )
        assert response1.status_code == 200
        
        # Act: Attempt duplicate signup
        response2 = client.post(
            f"/activities/{activity_name}/signup?email={new_email}",
            follow_redirects=True
        )
        
        # Assert
        assert response2.status_code == 400
        data = response2.json()
        assert data["detail"] == "Student already signed up"
