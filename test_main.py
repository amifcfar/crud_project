from urllib import response

from fastapi.testclient import TestClient

from main import app, inv_test

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_items():
    response = client.get("/items/")
    #assert response.status_code == 200
    assert response.json() == {"items": inv_test}


def test_get_item_by_id():
    response = client.get("/items/1")
   # assert response.status_code == 200
    assert response.json() == {"title": "puma", "description": "tout terrain", "price": 1000, "quantity": 50, "item_id": 1}


def test_get_item_by_id2():
    response = client.get("/items/2")
    #assert response.status_code == 200
    assert response.json() == {"title": "nike", "description": "puissant", "price": 2000, "quantity": 20, "item_id": 2}











