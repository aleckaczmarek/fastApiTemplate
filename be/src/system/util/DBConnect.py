 
from fastapi import HTTPException
from ravendb import DocumentStore 

from system.transporters.Result import Result
from system.util.HttpUtils import  handleError
from system.util.DomainInterface import DomainModel

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
            doc_dict = object.dict()
            print("doc dict add to connected ", doc_dict)
            keys_to_sort = DomainModel().dict()
            del keys_to_sort["Id"]
            del keys_to_sort["collection_name"]
            for key in keys_to_sort.keys():
                del doc_dict[key]
                #  TODO figure out why id is being added as "Secret" instead of 2
            print("doc dict add to connected  post", doc_dict)
            user_to_add = self.model.get_new_instance(**doc_dict)
            print("user to add post", user_to_add)
            self.session.store(user_to_add, key) 
            self.session.save_changes() 
            return Result().build("status","success").build("data","Created Successfully")
        except (Exception) as error: 
            print("error db connect ",error)
            return await handleError(error,"Error Creating DBConnect ")

    async def deleteFromConnectedCollection(self, key):
        try: 
            self.session.delete(key)
            self.session.save_changes()
            return Result().build("status","success").build("data","Deleted Successfully")
        except (Exception) as error: 
            print("error db connect ",error)
            return await handleError(error,"Error Deleting DBConnect")
    
    async def updateInConnectedCollection(self,object, key):
        try: 
            document =  self.session.load(key)  
            print("dco gotten type ", type(document))
            if  document is None or type(document) == None : 
                print("none found")
                return Result().build("status","error").build("clientErrorMessage","Error fetching document.").build("error","No Document Found.")
            else: 
                print("doc gotten ",document.dict()) 
                doc_dict = document.dict()
                for key in DomainModel().dict().keys():
                    del doc_dict[key]
                for key in doc_dict:
                    print("key ", key, " ",object.dict().get(key))
                    if(object.dict().get(key)!=None):
                        document.build(key,object.dict().get(key))
                self.session.save_changes()
                return Result().build("status","success").build("data","Updated Successfully")
        except (Exception) as error: 
            print("error db connect ",error)
            return await handleError(error,"Error Updating Document DBConnect") 

    async def getFromConnectedCollection(self, id):
        try:  
            query = self.session.query_collection(self.collectionName).where_equals("Id",id)
            results = query.get_query_result().results
            if results is None or len(results) is 0:
                return Result().build("status","error").build("clientErrorMessage","Error fetching document.").build("error","No Document Found.")
            return Result().build("status","success").build("data",{"query": results})
        except (Exception) as error: 
            print("error db connect ",error)
            return await handleError(error,"Error Getting Document DBConnect") 
    
    async def getWhereFromConnectedCollection(self,key,value):
        try: 
            print("get where from connected collection key value ", key, value)
            query = self.session.query_collection(self.collectionName).where_equals(key,value)
            results = query.get_query_result().results
            if results is None or len(results) is 0:
                return Result().build("status","error").build("clientErrorMessage","Error fetching document.").build("error","No Document Found.")
            print("get where from connected collection ", results)
            return Result().build("status","success").build("data",{"query": results})
        except (Exception) as error: 
            print("error db connect get ",error)
            return await handleError(error,"Error Getting Where DBConnect")
        
    
    async def getAllFromConnectedCollection(self): 
        try: 
            query = self.session.query_collection(self.collectionName)  
            results = query.get_query_result().results
            return Result().build("status","success").build("data",{"query":results}) 
        except (Exception) as error: 
            print("error db connect get all ",error)
            return await handleError(error,"Error Getting All DBConnect")
       
     