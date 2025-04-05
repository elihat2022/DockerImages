# Manage connections to the database
from pymongo import MongoClient

from decouple import config
# Load environment variables


MONGO = config('MONGO')
# Base de datos local
#db_client = MongoClient("mongodb://host.docker.internal:27017/").local

# Base de datos Produccion
db_client = MongoClient(MONGO).test



