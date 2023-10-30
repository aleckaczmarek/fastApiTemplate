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
    email_address: Optional[str] = None
    collection_name:str = "Users" 

    def __init__(self,Id=None, first_name=None, last_name=None, address_id=None, email_address=None,collection_name="Users"):
        print("user init")
        super().__init__(Id=Id, first_name=first_name, last_name=last_name, address_id=address_id, email_address=email_address,collection_name=collection_name)
    
    # def __init__(self,data):
    #     super().__init__(Id=data.Id, first_name=data.first_name, last_name=data.last_name, address_id=data.address_id, email_address=data.email_address)

    # def __init__(self):
    #     super().__init__(Id=None, first_name=None, last_name=None, address_id=None, email_address=None)

    def build(self,key,value):
        setattr(self,key,value)

    def __eq__(self, other):
        return self.Id == other.Id and self.first_name == other.first_name and \
            self.last_name == other.last_name and self.address_id == other.address_id and \
                self.email_address == other.email_address