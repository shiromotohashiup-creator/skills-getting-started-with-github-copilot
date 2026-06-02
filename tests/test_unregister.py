import pytest


class TestUnregister:
    """Test suite for /activities/{activity_name}/unregister endpoint."""

    def test_unregister_registered_student_success(self, client, clean_activities):
        """
        Arrange: Use an already registered student from initial data
        Act: Call unregister API
        Assert: Verify status 200, message correct, participant removed
        """
        # Arrange
        activity_name = "Chess Club"
        # From initial data: "michael@mergington.edu" is registered
        email = "michael@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in clean_activities[activity_name]["participants"]
        assert len(clean_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_multiple_students_success(self, client, clean_activities):
        """
        Arrange: Prepare multiple registered students from initial data
        Act: Unregister them sequentially
        Assert: Verify all removed correctly with status 200
        """
        # Arrange
        activity_name = "Programming Class"
        emails_to_remove = [
            "emma@mergington.edu",
            "sophia@mergington.edu"
        ]
        initial_count = len(clean_activities[activity_name]["participants"])
        
        # Act & Assert
        for email in emails_to_remove:
            response = client.delete(
                f"/activities/{activity_name}/unregister?email={email}",
                follow_redirects=True
            )
            assert response.status_code == 200
            assert email not in clean_activities[activity_name]["participants"]
        
        # Final assertion: verify count decreased by 2
        assert len(clean_activities[activity_name]["participants"]) == initial_count - 2

    def test_unregister_nonexistent_activity_404(self, client, clean_activities):
        """
        Arrange: Prepare a non-existent activity name
        Act: Attempt to unregister from that activity
        Assert: Verify status 404 with "Activity not found" message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_unregistered_student_400(self, client, clean_activities):
        """
        Arrange: Use an email not registered for this activity
        Act: Attempt to unregister them
        Assert: Verify status 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        # Use an email not in Chess Club participants
        unregistered_email = "unregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={unregistered_email}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student not registered for this activity"

    def test_unregister_already_unregistered_student_400(self, client, clean_activities):
        """
        Arrange: Unregister a student once
        Act: Attempt to unregister them again from the same activity
        Assert: Verify status 400 on second unregister attempt
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "sarah@mergington.edu"
        
        # First unregister (should succeed)
        response1 = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            follow_redirects=True
        )
        assert response1.status_code == 200
        
        # Act: Attempt to unregister again
        response2 = client.delete(
            f"/activities/{activity_name}/unregister?email={email}",
            follow_redirects=True
        )
        
        # Assert
        assert response2.status_code == 400
        data = response2.json()
        assert data["detail"] == "Student not registered for this activity"

    def test_unregister_participant_order_preserved(self, client, clean_activities):
        """
        Arrange: Activity with multiple participants
        Act: Remove one participant and verify others remain in order
        Assert: Remaining participants are in original order
        """
        # Arrange
        activity_name = "Programming Class"
        original_participants = clean_activities[activity_name]["participants"].copy()
        email_to_remove = original_participants[0]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email_to_remove}",
            follow_redirects=True
        )
        
        # Assert
        assert response.status_code == 200
        remaining = clean_activities[activity_name]["participants"]
        # Verify remaining participants are in original order (minus the removed one)
        expected_order = original_participants[1:]
        assert remaining == expected_order
