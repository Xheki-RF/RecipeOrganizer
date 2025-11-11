from app.schemas.schemas_recipe import User
from uuid import UUID

# Test user creation
def test_create_user(client):
    user_data = {
        "username": "Jane Doe",
        "email": "zenlesszone@gmail.com",
        "password": "furrylover"
    }

    response = client.post("/users/create_user", json=user_data)

    assert response.status_code == 200

    user = User(**response.json())

    assert user.username == "Jane Doe"
    assert user.email == "zenlesszone@gmail.com"
    assert isinstance(user.id, UUID)

# Test getting a list of all users
def test_get_users(client):
    user_data_1 = {
        "username": "Jane Doe",
        "email": "zenlesszone@gmail.com",
        "password": "furrylover",
    }

    response_1 = client.post("/users/create_user", json=user_data_1)

    assert response_1.status_code == 200

    user_data_2 = {
        "username": "Avian Birb",
        "email": "birb69@gmail.com",
        "password": "avianlover",
    }

    response_2 = client.post("/users/create_user", json=user_data_2)

    assert response_2.status_code == 200

    response_3 = client.get("/users/get_users")

    assert response_3.status_code == 200

    for test_user in response_3.json():
        user = User(**test_user)
