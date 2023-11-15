from requests import HTTPError
from src.repository.Repository import Repository   
from src.util.Middleware import Middleware
from src.transporters.Result import Result
from typing import Awaitable, Callable, T, Optional

from src.util.HttpUtils import HttpUtils
from src.transporters.Data import Data

class Service():
   
    def __init__(self, model):
         self.model = model
         self.httpUtils = HttpUtils()
         self.repo = Repository(model)
         self.middlewareRunner = Middleware().runner
    
    async def create(self,data,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def create(data):
            print("in service create ", data)
            if type(data) == Data:
               print("in data type Data ")
               return await self.repo.add(data.data)
            else:
               return await self.repo.add(data)
             
       try:
          result = await self.middlewareRunner(data,create,middleware)
          print("result create service", result)
          return result
       except Exception as error:
          return await self.httpUtils.handleError(error, "Error in service")
      

    async def getAll(self,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def getAll(data):
            return await self.repo.getAll()
       try:
            result =  await self.middlewareRunner(None,getAll,middleware)
            return result
       except Exception as error:
            return await self.httpUtils.handleError(error, "Error in service get all")

    async def get(self,data,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def get(data):
         if type(data) == Data:
            print("in data type Data " ,data.data.Id)
            return await self.repo.get(data.data.Id)
         else:
            print("in non type Data ", data)
            return await self.repo.get(data.Id)
       try:
            result =  await self.middlewareRunner(data,get,middleware)
            return result
       except Exception as error:
            return await self.httpUtils.handleError(error, "Error in service get")
    
    async def getWhere(self,key,value,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def getWhere(data):
            return await self.repo.getWhere(data['key'],data['value'])
      
       try:
          result = await self.middlewareRunner({"key":key,"value":value},getWhere,middleware)
          print("result getWhere service", result)
          return result
       except Exception as error:
          return await self.httpUtils.handleError(error, "Error in service")
  

    async def delete(self, id,middleware: Optional[Callable[..., Awaitable[T]]]):
       item = self.model()
       item.build("Id",id)
       def delete(data):
            return self.repo.delete(data.Id)
       result =  self.middlewareRunner(item,delete,middleware)
       return result

    async def update(self, data, middleware: Optional[Callable[..., Awaitable[T]]]):
       async def update(data): 
            print(" inside service update ", data)
            print("type of data ", type(data))
            if type(data) == Data:
               return await self.repo.update(data.data,data.data.Id)
            else:
               return await self.repo.update(data,data.Id)
       try:
          result =  await self.middlewareRunner(data,update,middleware) 
          return result
       except Exception as error:
          return await self.httpUtils.handleError(error, "Error in service")
 