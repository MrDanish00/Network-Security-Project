
from pymongo import MongoClient

uri = "mongodb+srv://danishamir00:NSecurity123@networksecurityproject.qky1eg8.mongodb.net/?appName=NetworkSecurityProject"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)