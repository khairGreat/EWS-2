import gridfs
import os
import certifi  # Fixes SSL errors
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# --- CONFIGURATION ---
URI = "mongodb+srv://user1:khair12345@cluster0.886rdzt.mongodb.net/forecast_db?retryWrites=true&w=majority"
DB_NAME = 'models_db'
LOCAL_MODEL_FOLDER = 'models' # The folder name where you want files saved

# 1. Setup Connection
# We use tlsCAFile=certifi.where() to ensure it works on any server/cloud
client = MongoClient(URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())

try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB successfully!")
    
    # 2. Connect to GridFS
    db = client[DB_NAME]
    fs = gridfs.GridFS(db)

    # 3. Find the LATEST file
    # Sort by 'uploadDate' descending (-1) to get the newest one
    latest_file = db['fs.files'].find_one(sort=[("uploadDate", -1)])

    if latest_file:
        # Get metadata from the database
        mongo_filename = latest_file['filename']
        file_id = latest_file['_id']
        upload_date = latest_file['uploadDate']
        
        print(f"🔎 Found latest model in DB: {mongo_filename}")
        print(f"📅 Uploaded on: {upload_date}")

        # 4. Construct Dynamic Path
        # os.getcwd() gets the current working directory of your project
        base_path = os.getcwd()
        # Join paths safely (works on Windows/Linux/Mac)
        full_folder_path = os.path.join(base_path, LOCAL_MODEL_FOLDER)
        
        # Create the directory if it doesn't exist
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)
            print(f"📂 Created new directory: {full_folder_path}")
            
        # Create the full file path
        final_file_path = os.path.join(full_folder_path, mongo_filename)

        # 5. Check if file already exists
        if os.path.exists(final_file_path):
            print(f"✋ Model already exists locally at: {final_file_path}")
            print("Skipping download.")
        else:
            # 6. Download and Save if it doesn't exist
            print(f"⬇️ Downloading to: {final_file_path}...")
            
            grid_out = fs.get(file_id)
            
            with open(final_file_path, 'wb') as f:
                f.write(grid_out.read())
                
            print(f"✅ Success! Model saved locally at: {final_file_path}")

    else:
        print("❌ No models found in the database.")

except Exception as e:
    print(f"❌ Error: {e}")