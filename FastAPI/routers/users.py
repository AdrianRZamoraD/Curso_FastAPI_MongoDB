### Users ###

from   fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Url Local: https://127.0.0.1:8000

router = APIRouter()

# inicia el server: uvicorn users:app --reload 

# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Adrian",surname="Zamora", url="https://adrian.zam", age=31), 
              User(id=2,name="ñonga", surname="la suya", url="https://ñonga.las", age=25),
              User(id=3,name="ñon", surname="ga",url="https://ñon.ga", age=39 )]


@router.get("/usersjson") # get = obtención de información de páginas establecidas reales
async def usersjson(): # Creamo un json a mano
    return [{"name":"Adrian", "surname":"Zamora", "url":"https://adrian.zam", "age":31},
            {"name":"ñonga", "surname":"la suya", "url":"https://ñonga.las", "age":25},
            {"name":"ñon", "surname":"ga", "url":"https://ñon.ga", "age":39}]

@router.get("/users")
async def users():
    return users_list

#Path

@router.get("/user/{id}") #/?id
async def user(id:int):
    return search_user(id)

# Query parámetro que ir o no ir

@router.get("/userquey/")
async def user(id:int): # name: str (/1&name=) el "&" se usa para concatenar información de la url
        return search_user(id)

# Post, para añadir

@router.post("/user/", response_model=User, status_code=201)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe") # raise, cambiamos el texto en código de programa
        
    
    users_list.append(user)
    return user

# put, para actualizar

@router.put("/user/")
async def user(user:User):

    found = False


    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return user     

# Delete, borrar información

@router.delete("/user/{id}")
async def user(id:int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"El usuario ha sido eliminado"}

    
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    

def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
