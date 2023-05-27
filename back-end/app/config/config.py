from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import find_dotenv, load_dotenv
import os


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


mongo_host = os.getenv('mongo_host')
mongo_port = os.getenv('mongo_port')
mongo_username = os.getenv('mongo_username')
mongo_password = os.getenv('mongo_password')
mongo_database = os.getenv('mongo_database')
mongo_collection = os.getenv('mongo_collection')


mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin&readPreference=secondary&directConnection=true&ssl=false"
try:
    client = MongoClient(mongo_uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=20000)
    db = client[mongo_database]
    collection = db[mongo_collection]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Failed to connect to MongoDB:", e)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

# client = MongoClient("mongodb+srv://dbAPIDashboard:dbAPIDashboard@cluster0.5iliejt.mongodb.net/?retryWrites=true&w=majority")
# conn = client.api_dashboard_application
# db=conn["api_dashboard"]