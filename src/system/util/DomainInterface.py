 
from ast import Dict
from pydantic import BaseModel  
from typing import Any, Optional

class DomainModel(BaseModel):
    Id: Optional[str] = None
    collection_name:Optional[str]  = None 
    locked:Optional[bool] = False
    secured_vars:Optional[str] = None
    secure:Optional[bool] = False

    class Config:
        orm_mode = True

    def filter_list(self, key, ignore_locked_key):
        if key is "Id": raise Exception("Id cannot change after instantiation.\n Use the model constructor to modify.")
        if key is "secure": raise Exception("Secure cannot change after instantiation.\n Use the model constructor to modify.")
        if key is "secured_vars": raise Exception("Secured_vars cannot change after instantiation.\n Use the model constructor to modify.")
        if key is "locked" and ignore_locked_key is not True: raise Exception("Use the .lock() function to lock the model.")
        if self.locked == True: raise Exception("You cannot build or change a model after it is locked.")
    
    def build(self,key,value):
        self.filter_list(key, False)
        setattr(self,key,value)
        return self
    
    def lock(self):
        setattr(self,"locked",True)
        return self
    
    def __setattr__(self, name, value):
        self.filter_list(name, True)
        self.__dict__[name] = value
        return self
    
    @classmethod
    def get_new_instance(cls, **kwargs ):
        return cls(**kwargs)
    
    def __eq__(self, other):
        return self.Id == other.Id

  
