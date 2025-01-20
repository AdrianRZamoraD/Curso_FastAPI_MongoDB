from fastapi import APIRouter

router = APIRouter(prefix="/products", # prefix indicamos que usando solo "/" se refiere a prodcuts  
                    tags=["products"], # tags te agrupa para ver mejor la infomración en swagger
                    responses={404: {"message": "No encontrado"}})

# uvicorn products:app --reload

product_list = ["producto 1", "producto 2", "producto 3", "producto 4", "producto 5"]

@router.get("/")
async def products():
    return product_list

@router.get("/{id}")
async def products(id:int):
    return product_list[id]