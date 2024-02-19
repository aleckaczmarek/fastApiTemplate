from pydantic import BaseModel
from typing import Optional, Union
from api.model import User, Contract
from system.transporters.Result import Result

class Data(BaseModel):
    data:  Optional[Union[ User.User, Contract.Contract  , Result ]] = None
    options: Optional[dict] = None
    
    def __init__(self, data={}, options={}):
        super().__init__(data=data, options=options)

    def build(self,key,value):
        setattr(self,key,value)
        return self
 