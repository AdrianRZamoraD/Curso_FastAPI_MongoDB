from pydantic import BaseModel
from typing import Optional # Para hacer que el id sea opcional y no nos lo solicite.

# Entidad User
class User(BaseModel):
    id: Optional[str] = None # "None" (opcional) para establecer que, puede que el id no nos llegue, por ser usuarios nuevos, se usa "str" para crear id únicos y mas largos
    username: str
    email: str

