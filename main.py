from typing import Union
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from peewee import SqliteDatabase, Model, CharField, DateField
from datetime import date


# people use FastAPI to make APIs (high performance) and async


app = FastAPI()  # makes an instance of the app

templates = Jinja2Templates(directory="templates")

db = SqliteDatabase("fastapi-demo.db")


# class User:
#     def __init__(self, id, name, birthday):
#         self.id = id
#         self.name = name
#         self.birthday = birthday

class User(Model):
    name = CharField(max_length=100)
    birthday = DateField()

    class Meta:
        database = db

# users = [
#     User(1, "Bart", "10/03/1971"),
#     User(2, "Mary", "01/01/2001")
# ]

db.connect()
db.create_tables([User])

try:
    user1 = User.select().where(User.name == "Bart").get()
except:
    user1 = User(name="Bart", birthday=date(1971,10,3))

try:
    user2 = User.select().where(User.name == "Mary").get()
except:
    user2 = User(name="Mary", birthday=date(2001,1,1))
    user2.save()




# like view functions with decorators
@app.get("/", response_class=HTMLResponse)  # need to tell it to accept HTML
def home(request: Request):  # type hinting; dependency injection

    # request.

    return templates.TemplateResponse("index.html", {"request": request})

    # return {"Hello": "World"}

    # below options do not work because only obtain json by default
    # return "<html><head></head><body><h1>Hello World</h1></body></html>"
    # return """<html>
    #             <head>
    #             </head>
    #             <body>
    #                 <h1>Hello World</h1>
    #             </body>
    #         </html>"""

# print(home.__annotations__)


@app.get("/users", response_class=HTMLResponse)
def users_list(request:Request):
    users = User.select()
    return templates.TemplateResponse("users/list.html", {"request": request, "users": users})


@app.get("/users/create")
def user_create(name: str = Form(), birthday:date = Form()):
    user = User(name=name, birthday=birthday)
    user.save()
    return RedirectResponse("/users")


@app.get("/users/create", response_class=HTMLResponse)
def user_create_form(request:Request):
    return templates.TemplateResponse("users/create.html", {"request": request})



@app.get("/users/{user_id}", response_class=HTMLResponse)
def users_details(request:Request, user_id: int):
    # found_user = None
    # for user in users:
    #     if user.id == user_id:
    #         found_user = user
    user = User.select().where(User.id == user_id).get()
    return templates.TemplateResponse("users/detail.html", {"request": request, "user": found_user})







# uvicorn main:app --reload  to run server
# localhost:8000/docs -- will show documents while interacting with site
# to use db with it -- advanced user guide (SQL (Relational) Databases with Peewee)
