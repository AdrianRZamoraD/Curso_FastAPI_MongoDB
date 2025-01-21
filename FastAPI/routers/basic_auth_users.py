### Basi auth users ###

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


# Url Local: https://127.0.0.1:8000

# OAuth2PasswordRequestForm, para capturar ususario y contraseña


router = APIRouter(prefix="/basic_auth", # prefix indicamos que usando solo "/" se refiere a prodcuts  
                    tags=["basic_auth"], # tags te agrupa para ver mejor la infomración en swagger
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password: str


users_db = {
    "Azwors": {
        "username": "Adrian",
        "full_name": "Adrian Zamora",
        "email": "Adr.Zam@hotmail.com",
        "disable": False,
        "password": "123456"

    },
    "Azwors2": {
        "username": "Adrian 2",
        "full_name": "Adrian Zamora 2",
        "email": "Adr.Zam@hotmail.com",
        "disable": True,
        "password": "654321"

    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = "Credenciales de autenticación inválidas",
            headers={"WWW-Authemticate":"Bearer"})
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail = "Usuario inactivo")
    
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"} # No entra user.username porque no estaba definido dentro de UserDB(User):
@router.get("/users/me")
async def me(user: User = Depends(current_user)): # Depends, operación que valide
    return user

