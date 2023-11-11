from pydantic import BaseModel
from typing import Optional

class Result(BaseModel):
    Id: Optional[int|str] = None
    status:  Optional[str] = None
    data: Optional[object] = None
    error: Optional[object] = None
    clientErrorMessage: Optional[object] = None
    middlewareData:Optional[object] = None

    def __init__(self,Id=None,status="pending", data={}, middlewareData={},error={},clientErrorMessage={}):
        super().__init__(Id=Id, status=status, data=data, middlewareData=middlewareData,error=error,clientErrorMessage=clientErrorMessage)

    def build(self,key,value):
        setattr(self,key,value)
        return self
 