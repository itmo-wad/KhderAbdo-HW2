from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Create or get the database
db = client['lab2']

# Create or get the collection (users)
accounts_collection = db['accounts']

#Inserting a new account
new_account = {
    'username': 'khderAbdo',
    'password': 'khder96268',
    'email': 'khder96ju@gmail.com',
    'university': 'ITMO'
}

# Insert into the collection
result = accounts_collection.insert_one(new_account)

if result.inserted_id:
    print("inserted successfully.")
else:
    print("not inserted.")
