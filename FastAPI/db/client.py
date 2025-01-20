
### MongoDB Client ###

# Módulo de conexión MongoDB: pip install pymongo
# Ejecución: mongod --dbpath C:\Users\ADZ_9\Directorios\MongoDB\data
# Use: Ctrl + C to stop mongodb in terminal, and uvicorn
# Conexión: mongodb://localhost
# Current IP address: 201.173.65.232 (Cluster00)
# username: adz93vd
# password: 654321Az

from pymongo import MongoClient

# Conexión a la base de datos local
# db_client = MongoClient("localhost").local # Al colocar .local ya se esta determinando la carpeta y no es necesario colocarlo en el código restante.

# Conexión para base de datos remota
db_client = MongoClient("mongodb+srv://adz93vd:654321Az@cluster00.t24ka.mongodb.net/?retryWrites=true&w=majority&appName=Cluster00").test