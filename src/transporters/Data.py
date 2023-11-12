from pydantic import BaseModel
from typing import Optional, Union
from src.model.User import User
from src.transporters.Result import Result 

class Data(BaseModel):
    data:  Optional[Union[User, Result]] = None
    options: Optional[dict] = None
    
    def __init__(self, data={}, options={}):
        super().__init__(data=data, options=options)

    def build(self,key,value):
        setattr(self,key,value)
        return self
 