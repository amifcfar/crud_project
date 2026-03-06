from fastapi.testclient import TestClient

from main import app, inv_test

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# def test_say_hello():
#     response = client.get("/say_hello/cedric")
#     #assert response.status_code == 200
#     assert response.json() == { "message": "Hello cedric" }

def test_get_item():
    response = client.get("/items/")
    #assert response.status_code == 200
    assert response.json() == {"items": inv_test}






