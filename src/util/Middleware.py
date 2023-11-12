from typing import Awaitable, Callable, T, Optional
from src.transporters.Result import Result
from src.util.HttpUtils import HttpUtils


class Middleware():
    def __init__(self): 
        self.httpUtils = HttpUtils()

    async def runner(self,data, method, middleware: Optional[Callable[..., Awaitable[T]]]|None):
        result = Result()
        try:
            if middleware != None:
                print("[ Middleware ] Starting Runner ", data , type(data) )
                result = await middleware(result,data) 
                print("middleware result ", result)
                if(result.status=="success"):
                    print("middleware success ", result)
                    print("middleware returned ", result.data)
                    result.build("middlewareData",result.data)
                    data =  await method(result.data)
                    print("method returned from middle ware with data ",data)
                    result.build("data", data)
                    return result
                elif(result.status=="error"):
                    print("middleware error ", result)
                    return result
                else:
                    print("error getting result from middleware, check middleware function, it must return an object with status and  data if status is success, or error if status is an error ")
                    return result
            else:
                dataInner = await method(data)
                print("returned runner, no middleware injected ", dataInner)
                result.build("data",dataInner)
                result.build("status","success")
                return dataInner
        except (Exception) as error:
            print("error in middleware runner with middleware as ", middleware, error) 
            return await self.httpUtils.handleError(error, "Error in middleware runner function")
     
