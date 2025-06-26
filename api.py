from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import pandas
from datetime import datetime

client = MongoClient('mongodb://mongo:27017/')
print("[*] Connection Established")

db = client["ESA"]
collection = db["results"]

app = FastAPI()

def serialize_doc(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@app.get("/check")
def check():
    return {"Connection" : True}

@app.get("/get")
def getfrom(start_time: str, end_time: str):
    print(f"=== API CALLED: {start_time} to {end_time} ===")
    
    try:
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        print(f"Parsed dates: {start_dt} to {end_dt}")
    except Exception as e:
        print(f"Date parse error: {e}")
        return {"success": False, "error": "date_parse_error"}
    
    cursor = collection.find({
        "timestamp": {"$gte": start_dt, "$lte": end_dt}
    }).sort("timestamp", 1)
    
    records = [serialize_doc(doc) for doc in cursor]
    
    print(f"Found {len(records)} records")
    
    if len(records) == 0:
        return {"success": False, "error": "no_data_in_range"}
    
    return {
        "success": True, 
        "count": len(records), 
        "data": records
    }

@app.get("/getexample")
async def getfirst(lim: int):
    cursor = collection.find().limit(lim)
    records = []
    for doc in cursor:
        records.append(serialize_doc(doc))
    return {
        "success": True,
        "data": records
    }

@app.get("/getall")
async def getcollection():
    cursor = collection.find().sort("timestamp", 1)
    records = []
    for doc in cursor:
        records.append(serialize_doc(doc))
    return {
        "success": True,
        "data": records
    }
