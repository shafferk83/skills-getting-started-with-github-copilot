import pytest


pytestmark = pytest.mark.anyio


async def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = await client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"

    activities_response = await client.get("/activities")
    activities_payload = activities_response.json()
    assert email in activities_payload[activity_name]["participants"]


async def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = await client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


async def test_signup_rejects_unknown_activity(client):
    # Arrange
    missing_activity = "Unknown Activity"
    email = "new.student@mergington.edu"

    # Act
    response = await client.post(f"/activities/{missing_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


async def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Basketball Team"
    enrolled_email = "alex@mergington.edu"

    # Act
    response = await client.delete(
        f"/activities/{activity_name}/signup", params={"email": enrolled_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {enrolled_email} from {activity_name}"

    activities_response = await client.get("/activities")
    activities_payload = activities_response.json()
    assert enrolled_email not in activities_payload[activity_name]["participants"]


async def test_unregister_rejects_unknown_activity(client):
    # Arrange
    missing_activity = "Unknown Activity"
    email = "test.student@mergington.edu"

    # Act
    response = await client.delete(
        f"/activities/{missing_activity}/signup", params={"email": email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


async def test_unregister_rejects_non_member(client):
    # Arrange
    activity_name = "Chess Club"
    non_member_email = "not.enrolled@mergington.edu"

    # Act
    response = await client.delete(
        f"/activities/{activity_name}/signup", params={"email": non_member_email}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not signed up for this activity"
