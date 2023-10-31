from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    def dataclass(model):
        return model
    
@dataclass
class User(BaseModel):
    Id: Optional[int|str] = None
    first_name:  Optional[str] = None
    last_name: Optional[str] = None
    address_id: Optional[int] = None 
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    collection_name:str = "users" 

    def __init__(self,Id=None, first_name=None, last_name=None, address_id=None, username=None, email=None, full_name=None, disabled=None, collection_name="Users"):
        print("user init")
        super().__init__(Id=Id, first_name=first_name, last_name=last_name, address_id=address_id, username=username, email=email, full_name=full_name,disabled=disabled,collection_name=collection_name)

    def build(self,key,value):
        setattr(self,key,value)

    def __eq__(self, other):
        return self.Id == other.Id and self.first_name == other.first_name and \
            self.last_name == other.last_name and self.address_id == other.address_id and \
                self.email_address == other.email_address