 
from fastapi import HTTPException
from ravendb import DocumentStore 

from system.transporters.Result import Result
from system.util.HttpUtils import  handleError

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
            print("starting collection connection ")
            self.store = DocumentStore(self.baseUrl, collectionName)
            self.collectionName = collectionName
            self.store.initialize()
            self.session = self.store.open_session()
            print("connection opened end ", self.store)
    
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
            return await handleError(error,"Error Creating ")

    async def deleteFromConnectedCollection(self, key):
        self.session.delete(key)
        self.session.save_changes()
    
    async def updateInConnectedCollection(self,object, key):
        try: 
            document =  self.session.load(key)  
            print("dco gotten type ", type(document))
            
            if  document is None or type(document) == None : 
                print("none found")
                return await handleError(None,"No Document Found To Update DBConnect")
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
            return await handleError(error,"Error Updating Document DBConnect") 

    async def getFromConnectedCollection(self, key):
        try:  
            print("about to get doc ",key) 
            document = self.session.load(key)  
            print("dco gotten type ", type(document))
            if  document is None or type(document) == None : 
                print("none found")
                return await handleError(None,"No Document Found To Get DBConnect")
            else: 
                print("doc gotten ",document)  
                return Result().build("status","success").build("data",{"query":document})
        except (Exception) as error: 
            print("error db connect ",error)
            return await handleError(error,"Error Getting Document DBConnect") 
    
    async def getWhereFromConnectedCollection(self,key,value):
        try: 
            query = self.session.query_collection(self.collectionName).where_equals(key,value)
            results = query.get_query_result().results
            return Result().build("status","success").build("data",{"query": results})
        except (Exception) as error: 
            print("error db connect get ",error)
            return await handleError(error,"Error Getting User DBConnect")
        
    
    async def getAllFromConnectedCollection(self): 
        try: 
            query = self.session.query_collection(self.collectionName)  
            results = query.get_query_result().results
            return Result().build("status","success").build("data",{"query":results}) 
        except (Exception) as error: 
            print("error db connect get all ",error)
            return await handleError(error,"Error Getting All DBConnect")
       
     