### Users DB API ###

# Url Local: https://127.0.0.1:8000

from fastapi import APIRouter, HTTPException, status
from db.Models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb", 
                    tags=["userdb"], 
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# inicia el server: uvicorn users:app --reload 
# inicia mongod: mongod --dbpath C:\Users\ADZ_9\Directorios\MongoDB\data 


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


#Path

@router.get("/{id}") #/?id
async def user(id:str):
    return search_user("_id", ObjectId(id))

# Query parámetro que ir o no ir

@router.get("/")
async def user(id:str): # name: str (/1&name=) el "&" se usa para concatenar información de la url
    return search_user("_id", ObjectId(id))

# Post, para añadir

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user:User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe") # raise, cambiamos el texto en código de programa

    user_dict = dict(user) # hay que ingresr al jonson un id para que lo pueda borrar y crear uno nuevo (el hacer caso omiso no funciona el post)
    del user_dict["id"] # para que el propio mongoDB se encargue de otorgar el id

    id = db_client.users.insert_one(user_dict).inserted_id # (user_dict)

    new_user = user_schema(db_client.users.find_one({"_id":id})) # MongoDB crea por default _id

    return User(**new_user)

# put, para actualizar

@router.put("/", response_model=User)
async def user(user:User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))     


# Delete, borrar información

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):

    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    

def search_user(field:str, key):
    
    try:
        user = db_client.users.find_one({field:key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}
