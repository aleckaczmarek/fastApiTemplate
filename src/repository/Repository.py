import os
from dotenv import load_dotenv
from src.util.DBConnect import DBConnect 
from src.model.Result import Result
load_dotenv()

class Repository():
    
    def __init__(self, model):
        BASE_DB_URL = os.getenv('BASE_DB_URL')
        print("base url db connect ", BASE_DB_URL)
        self.db = DBConnect(model, BASE_DB_URL)
        self.db.connectToCollection(model().collection_name)
        self.model=model
    
    def add(self, data):
        try:
            self.db.addToConnectedCollection(data,data.Id)
            return True
        except (Exception) as error:
            print(error)
            return False
     
    async def update(self, data, key):
        try:
            result =  await self.db.updateInConnectedCollection(data, key) 
            print ("repo update result ", result)
            return result
        except (Exception) as error: 
            raise error 
    
    def getAll(self): 
        try:
            documents = []
            query = self.db.getAllFromConnectedCollection()
            for doc in query:
                del doc['@metadata'] 
                newDoc = self.model()
                for key in doc:
                    newDoc.build(key,doc[key])
                documents.append(newDoc) 
            return documents
        except (Exception) as error:
            print("error repo")
            print(error)
            return None

    def get(self, id):
        try:
            document = self.db.getFromConnectedCollection(id)
            newDoc = self.model()
            for item in document:
                newDoc.build(item[0],item[1])
            return document
        except (Exception) as error:
            print(error)
            return None
        
    async def getWhere(self,key,value):
        try:
            documents = []
            query = self.db.getWhereFromConnectedCollection(key,value) 
            for doc in query:
                del doc['@metadata'] 
                newDoc = self.model()
                for key in doc:
                    newDoc.build(key,doc[key])
                documents.append(newDoc) 
            return documents
        except (Exception) as error:
            print("error repo")
            print(error)
            return None

    def delete(self, id):
        try:
            self.db.deleteFromConnectedCollection(id)
            return True
        except (Exception) as error:
            print(error)
            return False
