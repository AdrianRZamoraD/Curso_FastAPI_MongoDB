### Hola Mundo ###

# Documentación oficial: https://fastapi.tiangolo.com/es/

# Instala FastAPI: pip install "fastapi[all]"

from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# FastAPI es el framework capás de crear el API
# Thunder client para realizar peticiones a las API

app = FastAPI()

#Routers - Clase en video (08/12/2022): https://www.twitch.tv/videos/1673759045

app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.include_router(users_db.router)

# http://127.0.0.1:8000/static/images/Krystal_2.png
 
app.mount("/statico", StaticFiles(directory="static"), name ="static")

# Url Local: https://127.0.0.1:8000

@app.get("/") # get = obtención de información de páginas establecidas reales
async def root():
    return "¡Hola FastAPI!"

# Url Local: https://127.0.0.1:8000/url

@app.get("/url")
async def url():
    return {"url":"https://AdrianRZD.com/python"}

# inicia el server: uvicorn main:app --reload
# Detener el server: CTLR + C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Docuemntación con Redocly: http://127.0.0.1:8000/redoc

# Postman, aplicación gratuita para interactuar con un API, realizar una petición