from app.schemas.schemas_recipe import Recipe

# Test №1: Add recipe
def test_add_recipe(client, create_users, add_recipe):
    response_user = client.post("/users/create_user", json=create_users())

    assert response_user.status_code == 200

    recipe_data = add_recipe()
    recipe_data["user_id"] = response_user.json()["id"]

    response_recipe = client.post("/recipe/add_recipe", json=recipe_data)

    assert response_recipe.status_code == 200

    recipe = Recipe(**response_recipe.json())

    assert recipe.title == "Bread"
    assert recipe.description == "Allows you to make a fluffy bread"
    assert str(recipe.user_id) == response_user.json()["id"]


# Test №2: Delete recipe
def test_delete_recipe(client, create_users, add_recipe):
    response_user = client.post("/users/create_user", json=create_users())

    assert response_user.status_code == 200

    recipe_data = add_recipe()
    recipe_data["user_id"] = response_user.json()["id"]

    response_recipe = client.post("/recipe/add_recipe", json=recipe_data)

    assert response_recipe.status_code == 200

    data = response_recipe.json()

    response_delete_recipe = client.delete(f"/recipe/delete_recipe/{data["id"]}")

    assert response_delete_recipe.status_code == 200
    assert response_delete_recipe.json() == f"Recipe {data["title"]} with ID {data["id"]} has been deleted"


# Test №3: Get user's recipes
def test_get_user_recipes(client, create_users, add_recipe):
    response_user = client.post("/users/create_user", json=create_users())

    assert response_user.status_code == 200

    recipe_data = add_recipe(False)

    for recipe in recipe_data:
        recipe["user_id"] = response_user.json()["id"]

        response_recipe = client.post("/recipe/add_recipe", json=recipe)

        assert response_recipe.status_code == 200

    data = response_user.json()

    response_get_recipe = client.get(f"/recipe/get_user_recipes/{data["id"]}")

    assert response_get_recipe.status_code == 200


# Test №4: Update user's recipe
def test_update_user_recipe(client, create_users, add_recipe):
    response_user = client.post("/users/create_user", json=create_users())

    assert response_user.status_code == 200

    recipe_data = add_recipe()
    recipe_data["user_id"] = response_user.json()["id"]

    response_recipe = client.post("/recipe/add_recipe", json=recipe_data)

    assert response_recipe.status_code == 200

    new_title = {"title": "White bread"}
    new_title_description = {"title": "White bread", 
                             "description": "Allows you to make a nice white bread"}
    new_title_description_category = {
        "title": "White bread",
        "description": "Allows you to make a nice white bread",
        "category": "6ff72fbd-7e12-43d1-83fd-0d69448be1b0",
    }

    new_recipe_data = response_recipe.json()

    response_update_1 = client.patch(f"/recipe/update_user_recipe/{new_recipe_data["id"]}", json=new_title)

    assert response_update_1.status_code == 200

    response_update_2 = client.patch(f"/recipe/update_user_recipe/{new_recipe_data["id"]}", json=new_title_description)

    assert response_update_2.status_code == 200

    response_update_3 = client.patch(f"/recipe/update_user_recipe/{new_recipe_data["id"]}", json=new_title_description_category)

    assert response_update_3.status_code == 200


# Test №5: Get user's recipe
def test_get_user_recipe(client, create_users, add_recipe):
    response_user = client.post("/users/create_user", json=create_users())

    assert response_user.status_code == 200

    recipe_data = add_recipe()
    recipe_data["user_id"] = response_user.json()["id"]

    response_recipe = client.post("/recipe/add_recipe", json=recipe_data)

    assert response_recipe.status_code == 200

    response_get_user_recipe = client.get(f"/recipe/get_user_recipe/{response_recipe.json()["id"]}")

    assert response_recipe.status_code == 200

    recipe = Recipe(**response_get_user_recipe.json())

    assert recipe.title == "Bread"
    assert recipe.description == "Allows you to make a fluffy bread"
    assert str(recipe.user_id) == response_user.json()["id"]
