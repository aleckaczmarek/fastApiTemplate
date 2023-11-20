from pydantic import BaseModel, ValidationError, validator
from typing import Optional,List

class User(BaseModel):
    Id: Optional[str] = None
    first_name:  Optional[str] = None
    last_name: Optional[str] = None
    address_id: Optional[int] = None 
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    auths: Optional[List[str]] = None
    groups: Optional[List[str]] = None
    disabled: Optional[bool] = None
    collection_name:Optional[str]  = "users"
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True
        
    def build(self,key,value):
        setattr(self,key,value)
        return self

    def __eq__(self, other):
        return self.Id == other.Id and self.first_name == other.first_name and \
            self.last_name == other.last_name and self.address_id == other.address_id and \
                self.email_address == other.email_address
 
     
