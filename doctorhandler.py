import os
import urllib.parse
from bson.codec_options import CodecOptions
from bson.binary import STANDARD
import atexit
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


db_username = "doctor"    # admin username or doctor username
db_password = "1234"    # admin_pass or doctor_pass
uri = f"mongodb+srv://{db_username}:{db_password}@main.qxefh.mongodb.net/?retryWrites=true&w=majority&appName=main"
key_vault_database_name = "encryption"
key_vault_collection_name = "__keyVault"
key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
encrypted_database_name = "encryped_healthcare"
encrypted_collection_name = "c_01"

doctor_client = MongoClient(
    uri,server_api = ServerApi('1'))

patients_collection = doctor_client[encrypted_database_name][encrypted_collection_name]

def close_client():
    if doctor_client:
        doctor_client.close()
atexit.register(close_client)

def print_patient_records():    
    patient_records = patients_collection.find()
    for record in patient_records:  
        print(record)
if __name__ == "__main__":
    patient_records = patients_collection.find()
    for record in patient_records:  
        print(record)

                
    

