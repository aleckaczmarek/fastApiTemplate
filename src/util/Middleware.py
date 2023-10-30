from typing import Awaitable, Callable, T, Optional
from src.model.Result import Result


class Middleware():  
    async def runner(self,data, method, middleware: Optional[Callable[..., Awaitable[T]]]|None):
        result = Result()
        try:
         if middleware != None:
            result = await middleware(result,data)
            if(result.status=="success"):
               print("middleware success ", result)
               result.build("middlewareData",result.data)
               data = method(result.data) 
               result.build("data", data)
               return result
            elif(result.status=="error"):
                print("middleware error ", result)
                return result
            else:
               print("error getting result from middleware, check middleware function, it must return an object with status and  data if status is success, or error if there is an error status ")
               return result
         else:
            data = method(data)
            result.build("data",data)
            result.build("status","success")
            return result
        except (Exception) as error:
          result.status = "error"
          result.data = {}
          result.build("data",{})
          result.build("status","error")
          result.build("error",error)
          print("error getting result from middleware, check middle ware function")
          print(error) 
          return result
     
