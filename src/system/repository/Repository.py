import os
from dotenv import load_dotenv 
from system.util.DBConnect import DBConnect  
from system.util.HttpUtils import HttpUtils 
load_dotenv()

class Repository():
    
    def __init__(self, model):
        BASE_DB_URL = os.getenv('BASE_DB_URL')
        self.httpUtils = HttpUtils()
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
             return await self.httpUtils.handleError(error, "[ Error Repository ] Add") 
     
    async def update(self, data, key):
        try:
            result =  await self.db.updateInConnectedCollection(data, key) 
            print ("repo update result ", result)
            return result
        except (Exception) as error: 
            return await self.httpUtils.handleError(error, "[ Error Repository ] Update") 
    
    async def getAll(self): 
        try:
            documents = []
            response = await self.db.getAllFromConnectedCollection()
            print("getAll in repo ", response)

            if response.status is "error" :
                return response
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
            return await self.httpUtils.handleError(error, "[ Error Repository ] Get All") 

    async def get(self, id):
        try:
            response = await self.db.getFromConnectedCollection(id)
            if response.status is "error" :
                return response
            newDoc = self.model()
            print("new doc ", newDoc)
            for doc in response.data.get("query"): 
                newDoc.build(doc[0],doc[1])
            response.build("data",{"query":newDoc})
            return response
        except (Exception) as error:
            print(error)
            print("error repo")
            return await self.httpUtils.handleError(error, "[ Error Repository ] Get") 
        
    async def getWhere(self,key,value):
        try:
            documents = []
            query = self.db.getWhereFromConnectedCollection(key,value)
            if query.status is "error" :
                return query
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
            return await self.httpUtils.handleError(error, "[ Error Repository ] Get Where") 

    async def delete(self, id):
        try:
            response = await self.db.deleteFromConnectedCollection(id)
            if response.status is "error" :
                return response
            return response
        except (Exception) as error:
            print(error)
            return await self.httpUtils.handleError(error, "[ Error Repository ] Delete") 