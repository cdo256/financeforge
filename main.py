from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def ping_db():
    uri = "mongodb+srv://devansh88karia:wrQ02Ifp0FfTLZB7@cluster0.pzrjg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    ping_db()
    #app.run(host="0.0.0.0", port=8080)
