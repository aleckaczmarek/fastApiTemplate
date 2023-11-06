from fastapi import HTTPException
from ravendb import DocumentStore
from requests import HTTPError

from src.model.Result import Result
from src.util.HttpUtils import handleError

class DBConnect(): 
    # ie 'http://127.0.0.1:2222'
    def __init__(self, model, baseUrl):
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

    def addToConnectedCollection(self,object, key):
        self.session.store(object, key) 
        self.session.save_changes()

    def deleteFromConnectedCollection(self, key):
        document =  self.session.load(key)
        self.session.delete(key)
        self.session.save_changes()
    
    async def updateInConnectedCollection(self,object, key):
        try: 
            document =  self.session.load(key)  
            print("dco gotten type ", type(document))
            if  type(document) == None : 
                print("none found")
                return await handleError(None,"No Document Found To Update")
                raise  HTTPException(500,"No Document Found To Update")
            # elif  document == None : 
            #     print("none found")
            #     return await handleError(None,"No Document Found To Update")
            #     raise  HTTPException(500,"No Document Found To Update")
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
            return await handleError(error,"Error Updating Document") # Result().build("status","error").build("error",error)

    def getFromConnectedCollection(self, key):
        return self.session.load(key)
    
    def getWhereFromConnectedCollection(self,key,value):
         query = self.session.query_collection(self.collectionName).where_equals(key,value)
         return query.get_query_result().results
    
    def getAllFromConnectedCollection(self): 
        query = self.session.query_collection(self.collectionName) 
        return query.get_query_result().results

    def addToCollection(self, collectionName, object, key):
        self.connectToCollection(self,collectionName)
        self.addToConnectedCollection(self, object, key)
        self.endConnectionFromCollection(self)
    
    def getFromCollection(self, collectionName, key):
        self.connectToCollection(self,collectionName)
        document =  self.session.load(key)
        self.endConnectionFromCollection(self)
        return document
 