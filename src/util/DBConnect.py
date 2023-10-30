from ravendb import DocumentStore

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
    
    def updateInConnectedCollection(self,object, key):
        document =  self.session.load(key)
        for item in object:
            if(item[1]==None): break
            setattr(document,item[0],item[1]) 
        self.session.save_changes()

    def getFromConnectedCollection(self, key):
        return self.session.load(key)
    
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
 