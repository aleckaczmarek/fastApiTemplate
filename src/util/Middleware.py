from typing import Awaitable, Callable, T, Optional
from fastapi import HTTPException

from transporters.Result import Result
from util.HttpUtils import HttpUtils


class Middleware():
    def __init__(self): 
        self.httpUtils = HttpUtils()

    async def runner(self,data, method, middleware: Optional[Callable[..., Awaitable[T]]]|None):
        result = Result()
        try:
            if middleware is not None:
                print("[ Middleware ] Starting Runner ", data , type(data) )
                result = await middleware(result,data) 
                print("middleware result ", result)
                if(result.status=="success"):
                    print("middleware success ", result)
                    print("middleware returned ", result.data)
                    result.build("middlewareData",result.data)
                    data.build("data", result.data)
                    data =  await method(data)
                    print("method returned from middle ware with data ",data)
                    result.build("data", data)
                    return result
                elif(result.status=="error" and result.clientErrorMessage is not None and len(result.clientErrorMessage)  > 0 ):
                    # TODO find out how to check if dict is empty so none check above can be correct
                    print("type of clienterrormessage ",type(result.clientErrorMessage))
                    print("middleware error ", result) 
                    return result
                else:
                    print("error getting result from middleware, check middleware function, it must return an object with status and  data if status is success, or error if status is an error ")
                    # TODO add logic to return error here instead of result, 
                    # should notify programmer that their middleware function returned malformed instead of returning random malformed result
                    return Result().build("clientErrorMessage",{"Middleware returned malformed response."}).build("status","error").build("error",{"Middleware function returned malformed, if status success please return data :  { object | dict | string } , if status error please return error: { object | dict | string } and clientErrorMessage:  { object | dict | string } "})
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
     
