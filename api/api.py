from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Allow CORS from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all HTTP headers
)

# Initialize MongoDB client
client = MongoClient("mongodb://root:example@localhost:14145/")  # Update with your MongoDB URL and port

# Pydantic models for request bodies
class DatabaseModel(BaseModel):
    name: str

class CollectionModel(BaseModel):
    database_name: str
    collection_name: str

@app.get("/databases")
async def get_databases():
    try:
        # Fetch the list of all databases
        databases = client.list_database_names()

        # Filter out 'admin', 'local', and 'config' databases
        filtered_databases = [db for db in databases if db not in ('admin', 'local', 'config')]

        # Create a dictionary to store database names and their collection names
        database_info = {
            "databases": [],
            "collections": {}
        }

        # Retrieve collections for each filtered database
        for db_name in filtered_databases:
            database_info["databases"].append(db_name)
            db = client[db_name]
            collection_names = db.list_collection_names()
            database_info["collections"][db_name] = collection_names

        return database_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-database")
async def create_database(database: DatabaseModel):
    try:
        # Create a new database
        db_name = database.name
        if db_name in ('admin', 'local', 'config'):
            raise HTTPException(status_code=400, detail="Cannot create a database with a reserved name.")

        # This operation will create the database if it does not exist
        db = client[db_name]

        # MongoDB does not create a database until it contains a collection
        db.create_collection("temp_collection")
        db.drop_collection("temp_collection")

        return {"message": f"Database '{db_name}' created successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-collection")
async def create_collection(collection: CollectionModel):
    try:
        # Add a new collection to an existing database
        db_name = collection.database_name
        collection_name = collection.collection_name

        if db_name in ('admin', 'local', 'config'):
            raise HTTPException(status_code=400, detail="Cannot add a collection to a reserved database.")

        if db_name not in client.list_database_names():
            raise HTTPException(status_code=404, detail=f"Database '{db_name}' not found.")

        db = client[db_name]
        if collection_name in db.list_collection_names():
            raise HTTPException(status_code=400, detail=f"Collection '{collection_name}' already exists in database '{db_name}'.")

        # Create the collection
        db.create_collection(collection_name)

        return {"message": f"Collection '{collection_name}' created successfully in database '{db_name}'."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
