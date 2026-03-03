from fastapi import FastAPI, HTTPException, Request, Form, Depends, Query

from typing import Annotated

from fastapi.templating import Jinja2Templates

from fastapi.responses import RedirectResponse, HTMLResponse

from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select

#templating object

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

templates = Jinja2Templates(directory="templates")




class Product(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    title: str = Field(default=None)
    description: str = Field(default=None)
    price: float = Field(default=None)
    quantity: int = Field(default=None)



class Item(BaseModel):

    title: str
    description: str
    price: float
    quantity: int
    item_id: int


app = FastAPI()


#this ensure one session will be used per request
def get_session():
    with Session(engine) as session:
        yield session

#Create tables in the database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#create table and database on start
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


SessionDep = Annotated[Session, Depends(get_session)]





inventory = []



template_test = [{"title": "nike", "description": "puissant", "price": 2000, "quantity": 20, "item_id": 1}]

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


@app.get("/api/v2/items/")
async def get_items_api(request: Request):
    return templates.TemplateResponse(request = request, name= "items/items.html", context = {"template_test": template_test})


@app.get("/api/v2/items/add/")
async def add_item_api(request: Request):
    print("---------------In add_item_api-------------")
    return templates.TemplateResponse(request = request, name= "items/add_item.html", context = {"template_test": template_test})
@app.post("/api/v2/items/save/")
async def save_item_api(request: Request, name: str =Form() , price: str = Form() , description: str = Form() , quantity: int = Form() , item_id: int | None = Form(...)):

    print("---------------In save_item_api-------------")
    temp_item_id = len(template_test) + 1
    if request.method == "POST":
        try:
            print(f"the request method is {request.method}")
            print(f"----------the item name is : {name}")
            print(f"----------the item price is : {price}")
            print(f"----------the item description is : {description}")
            print(f"----------the item quantity is : {quantity}")
            new_item = dict(title=name, description=description, price=price, quantity=quantity, item_id=temp_item_id)

            template_test.append(new_item)
            print("the item was not found in the inventory. It was added------------")
            print(f"the size of the inventory is now ------------------ {len(template_test)}")

            return RedirectResponse("/api/v2/items/", status_code=303)
        except :
            return {"message": "Error with the form data"}



@app.get("/api/v2/items/update/{item_id}")
async def update_item_api(request: Request, item_id: int ):
    print("---------------In update_item_api-------------")
    try:

        for item in template_test:
            if item_id == item["item_id"]:
                print(f"the request method is {request.method}")
                print(f"----------the item title is : {item["title"]}")
                print(f"the item description is : {item["description"]}")
                print(f"the item price is : {item["price"]}")
                print(f"the item quantity is : {item["quantity"]}")
                return templates.TemplateResponse(request= request, name= "items/update_item_api.html", context = {"item": item})

    except :
        return {"message": "Error with the form data"}

    return RedirectResponse("/api/v2/items/", status_code=303)


@app.post("/api/v2/items/update/save")
async def save_updated_item_api(request: Request, item_id: int | None = Form(), name: str = Form(...), description: str = Form(...), quantity: int = Form(...), price: int = Form(...)):
    print("---------------In save updated_item_api-------------")
    try:
        print(f"the request method is {request.method}")
        print(f"----------the item title is : {name}")
        print(f"the item description is : {description}")
        print(f"the item price is : {quantity}")
        print(f"the item item_id is : {item_id}")
        print(f"the item price is : {price}")

        for item in template_test:
            if item["item_id"] == item_id:
                item["title"] = name
                item["description"] = description
                item["price"] = price
                item["quantity"] = quantity
                print(f"the item was found and updated. The inventory size is ------------------ {len(template_test)}")
                return RedirectResponse("/api/v2/items/", status_code=303)

    except :
        return {"message": "Error with the form data"}



#add a new item
@app.post("/api/v3/items/")
async def post_items_api_v3(session: SessionDep , item: Product) -> Product:
    print("---------------In post_items_api_v3-------------")
    session.add(item)
    session.commit()
    return item

#Get a list of item from the store
@app.get("/api/v3/items/")
async def get_items_api_v3(session: SessionDep , offset : int = 0 , limit : Annotated[ int , Query(le = 100 )] = 100 ) -> list[Product]:
    print("---------------In get_items_api_v3-------------")
    items = session.exec(select(Product).offset(offset).limit(limit)).all()
    return items

#Get item by id
@app.get("/api/v3/items/{id}")
async def get_an_item_api_v3(session:SessionDep, id: int) -> Product:
    print("---------------In get_items_api_v3-------------")
    item = session.exec(select(Product).where(Product.id == id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item

@app.delete("/api/v3/items/delete/")
async def delete_an_item_api_v3(session: SessionDep , id: int) -> Product:
    print("---------------In delete_an_item_api_v3-------------")
   # item = session.delete(select(Product).where(Item.id == id))
    #get the item first
    item = session.get(Product, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    #then delete the item
    session.delete(item)
    session.commit()
    return {"message": "Item deleted"}
@app.post("/api/v3/items/update/", response_model=Product)
async def update_item_api_v3(session : SessionDep , item : Product) :
    print("---------------In update_item_api_v3-------------")
    product = session.get(Product, item.id)
    if not product:
        raise HTTPException(status_code=404, detail="Item not found")
    #update the product
    product.title = item.title
    product.description = item.description
    product.price = item.price
    product.quantity = item.quantity
    session.add(product)
    session.commit()
    return item

























