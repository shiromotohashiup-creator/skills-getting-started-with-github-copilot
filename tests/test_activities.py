import pytest


class TestActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_all_activities_success(self, client, clean_activities):
        """
        Arrange: Initialize with known activities count (9 activities)
        Act: Call GET /activities
        Assert: Verify status 200 and correct number of activities returned
        """
        # Arrange
        expected_count = 9
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == expected_count

    def test_get_activities_contains_required_fields(self, client, clean_activities):
        """
        Arrange: Prepare expected fields for activity objects
        Act: Call GET /activities and extract a specific activity
        Assert: Verify all required fields (description, schedule, max_participants, participants)
        """
        # Arrange
        activity_name = "Chess Club"
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        activity = data[activity_name]
        
        for field in required_fields:
            assert field in activity, f"Missing field: {field}"

    def test_get_activities_chess_club_details(self, client, clean_activities):
        """
        Arrange: Prepare expected values for Chess Club from initial data
        Act: Call GET /activities and extract Chess Club
        Assert: Verify all details match expected values
        """
        # Arrange
        activity_name = "Chess Club"
        expected_description = "Learn strategies and compete in chess tournaments"
        expected_schedule = "Fridays, 3:30 PM - 5:00 PM"
        expected_max = 12
        expected_initial_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        activity = data[activity_name]
        
        assert activity["description"] == expected_description
        assert activity["schedule"] == expected_schedule
        assert activity["max_participants"] == expected_max
        assert activity["participants"] == expected_initial_participants

    def test_get_activities_empty_participants(self, client, clean_activities):
        """
        Arrange: Clear participants from an activity
        Act: Call GET /activities
        Assert: Verify activity with empty participants returns empty list
        """
        # Arrange
        activity_name = "Art Studio"
        # Clear participants for this test
        clean_activities[activity_name]["participants"].clear()
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        activity = data[activity_name]
        assert activity["participants"] == []
        assert isinstance(activity["participants"], list)

    def test_get_activities_participants_updated_after_signup(self, client, clean_activities):
        """
        Arrange: Perform a signup operation
        Act: Call GET /activities after signup
        Assert: Verify participants list is updated in the response
        """
        # Arrange
        activity_name = "Basketball Team"
        new_email = "new_player@mergington.edu"
        
        # Sign up a new student
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}",
            follow_redirects=True
        )
        assert signup_response.status_code == 200
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        activity = data[activity_name]
        assert new_email in activity["participants"]

    def test_get_activities_participants_updated_after_unregister(self, client, clean_activities):
        """
        Arrange: Perform an unregister operation
        Act: Call GET /activities after unregister
        Assert: Verify participants list is updated in the response
        """
        # Arrange
        activity_name = "Music Ensemble"
        email_to_remove = "marcus@mergington.edu"
        
        # Verify email is in participants initially
        assert email_to_remove in clean_activities[activity_name]["participants"]
        
        # Unregister the student
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister?email={email_to_remove}",
            follow_redirects=True
        )
        assert unregister_response.status_code == 200
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        activity = data[activity_name]
        assert email_to_remove not in activity["participants"]

    def test_get_activities_all_activities_present(self, client, clean_activities):
        """
        Arrange: Prepare list of all expected activity names
        Act: Call GET /activities
        Assert: Verify all activities are present in response
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Science Club",
            "Debate Team"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity_name in expected_activities:
            assert activity_name in data, f"Activity {activity_name} not found"
