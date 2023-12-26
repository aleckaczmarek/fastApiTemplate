import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import HTTPException 
from system.util.DBConnect import DBConnect  
from system.util.HttpUtils import handleError, returnErrorCheckResolver

class Repository():
    
    def __init__(self, model):
        BASE_DB_URL = os.getenv('BASE_DB_URL') 
        self.db = DBConnect(model, BASE_DB_URL)
        self.db.connectToCollection(model().collection_name)
        self.model=model
    
    async def add(self, data):
        try:
            print("in try add about ")
            result = await self.db.addToConnectedCollection(data,data.Id)
            print("result from addToConnectedCOllection in repo ", result)
            if await returnErrorCheckResolver(result):
                return result 
            # Logic here if needed
            return result
        except (Exception) as error:
             return await handleError(error, "[ Error Repository ] Add") 
     
    async def update(self, data, key):
        try:
            result =  await self.db.updateInConnectedCollection(data, key) 
            print ("repo update result ", result)
            if await returnErrorCheckResolver(result):
                return result 
            # Logic here if needed
            return result
        except (Exception) as error: 
            return await handleError(error, "[ Error Repository ] Update") 
    
    async def getAll(self): 
        try:
            documents = []
            response = await self.db.getAllFromConnectedCollection()
            print("getAll in repo ", response)

            if await returnErrorCheckResolver(response):
                return response 
            #TODO update so we can get filter list from model directly, make filter list uneditable by builder 
            for doc in response.data.get("query"):
                del doc['@metadata'] 
                del doc['hashed_password'] 
                newDoc = self.model(**doc)
                documents.append(newDoc) 
            response.build("data",{"query":documents})
            return response
        except (Exception) as error:
            print("error repo")
            print(error)
            return await handleError(error, "[ Error Repository ] Get All") 

    async def get(self, id):
        try:
            documents = []
            result = await self.db.getFromConnectedCollection(id)
            if await returnErrorCheckResolver(result):
                return result 
            for doc in result.data.get("query"):
                print("doc in result.data.get  ", doc)
                del doc['@metadata'] 
                newDoc = self.model(**doc)
                documents.append(newDoc) 
            return documents
        except (Exception) as error:
            print(error)
            print("error repo")
            return await handleError(error, "[ Error Repository ] Get") 
        
    async def getWhere(self,key,value):
        try:
            documents = []
            result = await self.db.getWhereFromConnectedCollection(key,value)
            print("object get where  result", result)
            print("object type get where ", type(result))
            if await returnErrorCheckResolver(result):
                return result 
            for doc in result.data.get("query"):
                print("doc in result.data.getwhere", doc)
                del doc['@metadata'] 
                newDoc = self.model(**doc)
                documents.append(newDoc) 
            return documents
        except (Exception) as error:
            print("error repo")
            print(error)
            return await handleError(error, "[ Error Repository ] Get Where") 

    async def delete(self, id):
        try:
            response = await self.db.deleteFromConnectedCollection(id)
            if await returnErrorCheckResolver(response):
                return response
            # Logic here if needed
            return response
        except (Exception) as error:
            print(error)
            return await handleError(error, "[ Error Repository ] Delete") 
