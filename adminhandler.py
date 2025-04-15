import os
import urllib.parse
from bson.codec_options import CodecOptions
from bson.binary import STANDARD
import atexit
import pymongo
from pymongo.encryption import ClientEncryption
from pymongo.encryption_options import AutoEncryptionOpts
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# KMS provider name should be one of the following: "aws", "gcp", "azure", "kmip" or "local"
kms_provider_name = "local"    # "<KMS provider name>

db_username = "varunpratapsinghbhadoria"    # admin username or doctor username
db_password = "12345"    # admin_pass or doctor_pass

uri = f"mongodb+srv://{db_username}:{db_password}@main.qxefh.mongodb.net/?retryWrites=true&w=majority&appName=main"
key_vault_database_name = "encryption"
key_vault_collection_name = "__keyVault"
key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
encrypted_database_name = "encryped_healthcare"
encrypted_collection_name = "c_01"

# retrieve CMK and specify provider settings

path = "./customer-master-key.txt"
with open(path, "rb") as f:
    local_master_key = f.read()
    if len(local_master_key) != 96:
        raise Exception("Expected the customer master key file to be 96 bytes.")
    kms_provider_credentials = {
        "local": {
            "key": local_master_key
        },
    }

# set automatic encryption options

auto_encryption_options = AutoEncryptionOpts(
    kms_provider_credentials,
    key_vault_namespace,
    crypt_shared_lib_path="/home/malakh/Downloads/mongo_crypt_shared_v1-linux-x86_64-enterprise-ubuntu2404-8.0.5/lib/mongo_crypt_v1.so" 
)

# create new client to setup encrypted collection
encrypted_client = MongoClient(
    uri, auto_encryption_opts=auto_encryption_options)

# Specify Fields to Encrypt

encrypted_fields_map = {
  "fields": [
    {
        "path": "Phone",
        "bsonType": "string",
        "queries": { "queryType": "equality" }
    },
    {
        "path": "password",
        "bsonType" : "string",
        "queries" : { "queryType" : "equality" }
    }
    
  ]
}


encrypted_collection = encrypted_client[encrypted_database_name][encrypted_collection_name]
def close_client():
    if encrypted_client:
        encrypted_client.close()
atexit.register(close_client)
def encrypted_collection_insert(patient_document):
    result = encrypted_collection.insert_one(patient_document)
    return result

def encrypted_collection_find(patient_document):
    find_result = encrypted_collection.find_one(patient_document)
    return find_result

if __name__ == "__main__":
    
    encrypted_collection_insert(patient_document)
    find_result = encrypted_collection_find({"DemographicData.Name": "Varun Atkinson"})
    print(find_result)  

