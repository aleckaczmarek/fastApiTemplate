from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional, TYPE_CHECKING


class User(BaseModel):
    Id: Optional[int|str] = None
    first_name:  Optional[str] = None
    last_name: Optional[str] = None
    address_id: Optional[int] = None 
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    collection_name:Optional[str]  = "users"

    class Config:
        orm_mode = True
        
    def build(self,key,value):
        setattr(self,key,value)

    def __eq__(self, other):
        return self.Id == other.Id and self.first_name == other.first_name and \
            self.last_name == other.last_name and self.address_id == other.address_id and \
                self.email_address == other.email_address