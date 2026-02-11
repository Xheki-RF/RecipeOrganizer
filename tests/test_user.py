from app.schemas.schemas_recipe import User
from uuid import UUID


# Test №1: Create user
def test_create_user(client, create_users):
    response = client.post("/users/create_user", json=create_users())

    assert response.status_code == 200

    user = User(**response.json())

    assert user.username == "Jane Doe"
    assert user.email == "zenlesszone@gmail.com"
    assert isinstance(user.id, UUID)


# Test №2: Get user by ID
def test_get_user(client, create_users):
    response = client.post("/users/create_user", json=create_users())

    assert response.status_code == 200

    data = response.json()

    response_get = client.get(f"/users/get_user/{data['id']}")

    assert response_get.status_code == 200

    user = User(**response_get.json())

    assert user.username == "Jane Doe"
    assert user.email == "zenlesszone@gmail.com"


# Test №3: Get a list of all users
def test_get_users(client, create_users):
    for data in create_users(False):
        response = client.post("/users/create_user", json=data)

        assert response.status_code == 200

    response_get = client.get("/users/get_users")

    assert response_get.status_code == 200

# Test №4: Delete user
def test_delete_user(client, create_users):
    response = client.post("/users/create_user", json=create_users())

    assert response.status_code == 200

    data = response.json()

    delete_response = client.delete(f"/users/delete_user/{data['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json() == f"User {data['username']} with ID {data['id']} has been deleted"

# Test №5: Update user data
def test_update_user(client, create_users):
    response = client.post("/users/create_user", json=create_users())

    assert response.status_code == 200

    data = response.json()

    new_username = {"username": "Jade Joe"}
    new_name_password = {"username": "Jode Joe", "password": "Goyda369"}

    response_update = client.patch(f"/users/update_user_data/{data['id']}", json=new_username)

    assert response_update.status_code == 200
    assert response_update.json()["username"] == "Jade Joe"

    response_update = client.patch(f"/users/update_user_data/{data['id']}", json=new_name_password)

    assert response_update.status_code == 200
    assert response_update.json()["username"] == "Jode Joe"