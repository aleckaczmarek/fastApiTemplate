from pydantic import BaseModel
from typing import Optional

class Data(BaseModel):
    Id: Optional[int|str] = None
    data: Optional[object] = None
    options: Optional[object] = None

    def __init__(self,Id=None,  data={}, options={}):
        super().__init__(Id=Id,  data=data, options=options)

    def build(self,key,value):
        setattr(self,key,value)
        return self
 