import pyarrow as pyarrow
import pandas as pandas 
from pymongo import MongoClient

file = pandas.read_parquet("results.parquet")
datadict = file.to_dict(orient='records')

client = MongoClient("mongodb://mongo:27017/")
client.admin.command('ping')
print("[*] Connection Established")

db = client["ESA"]
collection = db["results"]

res = collection.insert_many(datadict)
print(f"[+] {len(res.inserted_ids)} inserted into collection")
collection.create_index("timestamp")
print("[*] All records sorted")

