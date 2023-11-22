import os
from dotenv import load_dotenv
from requests import HTTPError
from src.util.DBConnect import DBConnect 
from src.transporters.Result import Result
from src.util.HttpUtils import HttpUtils 
load_dotenv()

class Repository():
    
    def __init__(self, model):
        BASE_DB_URL = os.getenv('BASE_DB_URL')
        self.httpUtils = HttpUtils()
        print("base url db connect ", BASE_DB_URL)
        self.db = DBConnect(model, BASE_DB_URL)
        self.db.connectToCollection(model().collection_name)
        self.model=model
    
    async def add(self, data):
        try:
            print("in try add about ")
            result = await self.db.addToConnectedCollection(data,data.Id)
            print("result from addToConnectedCOllection in repo ", result)
            return result
        except (Exception) as error:
             return await self.httpUtils.handleError(error, "Error in repo") 
     
    async def update(self, data, key):
        try:
            result =  await self.db.updateInConnectedCollection(data, key) 
            print ("repo update result ", result)
            return result
        except (Exception) as error: 
            return await self.httpUtils.handleError(error, "Error in repo") 
    
    async def getAll(self): 
        try:
            documents = []
            response = await self.db.getAllFromConnectedCollection()
            print("getAll in repo ", response)
            #TODO update so we can get filter list from model directly, make filter list uneditable by builder 
            for doc in response.data.get("query"):
                del doc['@metadata'] 
                del doc['hashed_password'] 
                newDoc = self.model()
                for key in doc:
                    newDoc.build(key,doc[key])
                documents.append(newDoc) 
            response.build("data",{"query":documents})
            return response
        except (Exception) as error:
            print("error repo")
            print(error)
            return None

    async def get(self, id):
        try:
            response = await self.db.getFromConnectedCollection(id)
            newDoc = self.model()
            print("new doc ", newDoc)
            for doc in response.data.get("query"): 
                newDoc.build(doc[0],doc[1])
            response.build("data",{"query":newDoc})
            return response
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

    async def delete(self, id):
        try:
            await self.db.deleteFromConnectedCollection(id)
            return True
        except (Exception) as error:
            print(error)
            return False
