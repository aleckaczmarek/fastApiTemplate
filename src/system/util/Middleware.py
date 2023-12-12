from typing import Awaitable, Callable, T, Optional

from fastapi import HTTPException 

from system.transporters.Result import Result
from system.util.HttpUtils import HttpUtils


class Middleware():
    def __init__(self): 
        self.httpUtils = HttpUtils()

    async def runner(self,data, method, middleware: Optional[Callable[..., Awaitable[T]]]|None):
        result = Result()
        if middleware is not None:
            try:
                print("[ Middleware ] Starting Runner ", data , type(data) )
                result = await middleware(result,data) 
                print("[ Middleware ] middleware result ", result)
                if(result.status=="success"):
                    print("[ Middleware ] middleware success ",middleware, result)
                    print("[ Middleware ] middleware returned ", result.data)
                    result.build("middlewareData",result.data)
                    data.build("data", result.data)
                    data =  await method(data)
                    print("[ Middleware ] method returned from middle ware with data ", method, data)
                    # // TODO add status.error error check here
                    if type(data) is Result and data.status is "error":
                        return data
                    result.build("data", data)
                    return result
                elif(result.status=="error" and result.clientErrorMessage is not None and len(result.clientErrorMessage)  > 0 ):
                    # TODO find out how to check if dict is empty so none check above can be correct
                    print("[ Middleware ] type of clienterrormessage ",type(result.clientErrorMessage))
                    print("[ Middleware ] middleware error ", result) 
                    return result
                else:
                    print("[ Middleware ] error getting result from middleware, check middleware function, it must return an object with status and  data if status is success, or error if status is an error ")
                    return Result().build("clientErrorMessage",{"Middleware returned malformed response."}).build("status","error").build("error",{"Middleware function returned malformed, if status success please return data :  { object | dict | string } , if status error please return error: { object | dict | string } and clientErrorMessage:  { object | dict | string } "})
                  
            except Exception as error:
                print("[ Middleware ] error in middleware runner with middleware as ... and method as ... ", middleware, method, error) 
                return await self.httpUtils.handleError(error, "[ Middleware ] Error in middleware, Exception.")
        else:
            try:
                dataInner = await method(data)
                print("[ Middleware ] returned middleware runner, with middleware injected middleware as NONE INJECTED ",method, dataInner)
                result.build("data",dataInner)
                result.build("status","success")
                return dataInner
            except (Exception) as error:
                print("[ Middleware ]  error in middleware runner with middleware as NONE INJECTED ", middleware, method, error) 
                return await self.httpUtils.handleError(error, "[ Middleware ] Error in middleware.")
     
