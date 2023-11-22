from fastapi import HTTPException
from ravendb import DocumentStore 

from src.transporters.Result import Result
from src.util.HttpUtils import  HttpUtils

class DBConnect(): 
    # ie 'http://127.0.0.1:2222'
    def __init__(self, model, baseUrl):
         self.httpUtils = HttpUtils()
         self.model=model
         self.baseUrl=baseUrl

    # ie 'users'
    def connectToCollection(self, collectionName):
        try:
            self.endConnectionFromCollection(self)
            print("disconnected")
        except:
            print("no connection to disconnect")
        finally:
            self.store = DocumentStore(self.baseUrl, collectionName)
            self.collectionName = collectionName
            self.store.initialize()
            self.session = self.store.open_session()
    
    def endConnectionFromCollection(self):
        self.session.close()
        self.store.close()

    async def addToConnectedCollection(self,object, key):
        try: 
            self.session.store(object, key) 
            self.session.save_changes() 
            return Result().build("status","success").build("data","Created Successfully")
        except (Exception) as error: 
            print("error db connect ",error)
            return await self.httpUtils.handleError(error,"Error Creating ")

    async def deleteFromConnectedCollection(self, key):
        document =  self.session.load(key)
        self.session.delete(key)
        self.session.save_changes()
    
    async def updateInConnectedCollection(self,object, key):
        try: 
            document =  self.session.load(key)  
            print("dco gotten type ", type(document))
            if  document is None or type(document) == None : 
                print("none found")
                return await self.httpUtils.handleError(None,"No Document Found To Update DBConnect")
            else: 
                print("doc gotten ",document.dict()) 
                for key in object.dict():
                    print("key ", key, " ",object.dict().get(key))
                    if(object.dict().get(key)!=None):
                        document.build(key,object.dict().get(key))
                self.session.save_changes()
                return Result().build("status","success").build("data","Updated Successfully")
        except (Exception) as error: 
            print("error db connect ",error)
            return await self.httpUtils.handleError(error,"Error Updating Document DBConnect") # Result().build("status","error").build("error",error)

    async def getFromConnectedCollection(self, key):
        try: 
            results = self.session.load(key)
            return Result().build("status","success").build("data",{"query":results})
        except (Exception) as error: 
            print("error db connect get ",error)
            return await self.httpUtils.handleError(error,"Error Getting User DBConnect")
    
    def getWhereFromConnectedCollection(self,key,value):
         query = self.session.query_collection(self.collectionName).where_equals(key,value)
         return query.get_query_result().results
    
    async def getAllFromConnectedCollection(self): 
        try: 
            query = self.session.query_collection(self.collectionName)  
            results = query.get_query_result().results
            return Result().build("status","success").build("data",{"query":results})
        except (Exception) as error: 
            print("error db connect get all ",error)
            return await self.httpUtils.handleError(error,"Error Getting All DBConnect")
       

    def addToCollection(self, collectionName, object, key):
        self.connectToCollection(self,collectionName)
        self.addToConnectedCollection(self, object, key)
        self.endConnectionFromCollection(self)
    
    def getFromCollection(self, collectionName, key):
        self.connectToCollection(self,collectionName)
        document =  self.session.load(key)
        self.endConnectionFromCollection(self)
        return document
 