 
from typing import Awaitable, Callable, T, Optional

from fastapi import HTTPException

from system.repository.Repository import Repository   
from system.util.Middleware import middlewareRunner 
from system.util.HttpUtils import handleError
from system.transporters.Data import Data

class Service():
    def __init__(self, model):
         self.model = model 
         self.repo = Repository(model)
           
    async def create(self,data,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def create(data):
            print("in service create ", data)
            if type(data) == Data:
               print("in data type Data ")
               return await self.repo.add(data.data)
            else:
               return await self.repo.add(data)
       try:
          result = await middlewareRunner(data,create,middleware)
          print("result create service", result)
          return result
       except Exception as error:
          return await handleError(error, "[ Error Service ] Create")
      

    async def getAll(self,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def getAll(data): 
            return await self.repo.getAll()
       try:
            result =  await middlewareRunner(None,getAll,middleware)
            return result
       except Exception as error:
            return await handleError(error, "[ Error Service ] Get All")

    async def get(self,data,middleware: Optional[Callable[..., Awaitable[T]]]):
      #  TODO, determine if type check is still needed. Since adding options dict I think it is not.
      # You can also filter the middlewareData object inside the data var injected in the get(data) method here.
      # Maybe add a filter list here somehow to grab from the model? Or in the service?
       async def get(data):
         if type(data) == Data:
            print("in data type Data " ,data.data.Id)
            return await self.repo.get(data.data.Id)
         else:
            print("in non type Data ", data)
            return await self.repo.get(data.Id)
       try:
          
            result =  await middlewareRunner(data,get,middleware)
            return result
       except Exception as error:
            return await handleError(error, "[ Error Service ] Get")
    
    async def getWhere(self,key,value,middleware: Optional[Callable[..., Awaitable[T]]]):
       async def getWhere(data):
            return await self.repo.getWhere(data['key'],data['value'])
       try:
          result = await middlewareRunner({"key":key,"value":value},getWhere,middleware)
          print("result getWhere service", result)
          return result
       except Exception as error:
          return await handleError(error, "[ Error Service ] Get Where")
  

    async def delete(self, id,middleware: Optional[Callable[..., Awaitable[T]]]):
       item = self.model()
       item.build("Id",id)
       async def delete(data):
            return await self.repo.delete(data.Id)
       result =  middlewareRunner(item,delete,middleware)
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
          result =  await middlewareRunner(data,update,middleware) 
          return result
       except Exception as error:
          return await handleError(error, "[ Error Service ] Update")
 