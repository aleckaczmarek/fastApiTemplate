from requests import HTTPError
from src.repository.Repository import Repository   
from src.util.Middleware import Middleware
from src.model.Result import Result
from typing import Awaitable, Callable, T, Optional

from src.util.HttpUtils import handleError

class Service():

    def __init__(self, model):
         self.model = model
         self.repo = Repository(model)
         self.middlewareRunner = Middleware().runner
    
    def create(self,data,middleware: Optional[Callable[..., Awaitable[T]]]):
       def create(data):
            return self.repo.add(data)
       result =  self.middlewareRunner(data,create,middleware)
       return result

    async def getAll(self,middleware: Optional[Callable[..., Awaitable[T]]]):
       def getAll(data):
            return self.repo.getAll()
       result =  await self.middlewareRunner(None,getAll,middleware)
       return result

    async def get(self,id,middleware: Optional[Callable[..., Awaitable[T]]]):
       item = self.model()
       item.build("Id",id)
       def get(data):
            return self.repo.get(data.Id)
       result =  await self.middlewareRunner(item,get,middleware)
       return result
    
    async def getWhere(self,key,value,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def getWhere(data):
            return await self.repo.getWhere(data['key'],data['value'])
       result =  await self.middlewareRunner({"key":key,"value":value},getWhere,middleware)
       print("result ", result)
       return result

    async def delete(self, id,middleware: Optional[Callable[..., Awaitable[T]]]):
       item = self.model()
       item.build("Id",id)
       def delete(data):
            return self.repo.delete(data.Id)
       result =  self.middlewareRunner(item,delete,middleware)
       return result

    async def update(self, data, middleware: Optional[Callable[..., Awaitable[T]]]):
       async def update(data): 
            return await self.repo.update(data,data.Id)
       try:
          result =  await self.middlewareRunner(data,update,middleware) 
          return result
       except Exception as error:
          return await handleError(error, "Error in service")
 