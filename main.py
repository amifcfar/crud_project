from fastapi import FastAPI

from pydantic import BaseModel

class Item(BaseModel):

    title: str
    description: str
    price: float
    quantity: int
    item_id: int


app = FastAPI()

inventory = []

inv_test = [{"title": "puma", "description": "tout terrain", "price": 1000, "quantity": 50, "item_id": 1}, {"title": "nike", "description": "puissant", "price": 2000, "quantity": 20, "item_id": 2}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/items/")
async def get_items():
    return {"items": inv_test}

@app.get("/items/{item_id}")
async def get_item_by_id(item_id: int):
    if item_id > 0 and len(inv_test) > 0:
        for item in inv_test:
            if item["item_id"] == item_id:
                return item
    return {"message": "bad request, try again"}

@app.get("/items/{title}")
async def get_item_by_title(title: str):
    if len(title) > 0 and len(inv_test) > 0:
        for item in inv_test:
            if item["title"] == title:
                return item
    return {"message": "bad request, try again"}

@app.post("/items/add/")
async def add_item(item : Item):
    print("---------------In add_item--------------")
    if item is not None:
        #print item title
        print(f"the item title is {item.title}")
        print(f"the item description is {item.description}")
        print(f"the item price is {item.price}")
        print(f"the item quantity is {item.quantity}")
        inv_test.append(dict(title=item.title, description=item.description, price=item.price, quantity=item.quantity , item_id=item.item_id))
        print(f"--------------------the inventory size is now: {len(inv_test)}")

    return {"message": "The item was successfully added"}
@app.put("/items/update/")
async def update_item(item : Item):
    print("---------------In update_item-------------")
    if item:
        try:
            print(f"the item title is {item.title}")
            print(f"the item description is {item.description}")
            print(f"the item price is {item.price}")
            print(f"the item quantity is {item.quantity}")
            print(f"the item id is {item.item_id}")
            for merch in inv_test:
                print("--------------checking item in inventory-------------")
                if merch["item_id"] == item.item_id:
                    print("----------the item was found in the inventory----------------")
                    merch["title"] = item.title
                    merch["description"] = item.description
                    merch["price"] = item.price
                    merch["quantity"] = item.quantity
                    print("------------the item was updated in the inventory-------------")
                    return {"message": "The item was successfully updated"}
        except :
            return {"message": "the item was not updated in the inventory"}
    else:
        inv_test.append(dict(title=item.title, description=item.description, price=item.price, quantity=item.quantity , item_id=item.item_id))
        print("the item was not found in the inventory-------------")
        return {"message": "-----------------the item was added to the  inventory"}


    return {"message": "bad request, try again"}

@app.delete("/items/remove/{item_id}")
async def remove_item_by_id(item_id: int):
    print("---------------In remove_item_by_id-------------")
    if item_id > 0 and len(inv_test) > 0:
        for item in inv_test:
            if item["item_id"] == item_id:
                print("-------------the item was found in the inventory-------------")
                inv_test.remove(item)
                return {"message": "The item was successfully removed"}
    return {"message": "the item was not found in the inventory-------------"}


