from typing import Optional
from fastapi import HTTPException 
from src.transporters.Result import Result

class HttpUtils():
    async def runner(self,run,middleware):
        result =  await run(middleware)
        if result.status=="success":
            return result
        elif result.status=="error":
            return await self.handleError(result, None)
        else:
            return None
        
    async def runnerWithData(self,run,data,middleware):
        result =  await run(data,middleware) 
        if result.status=="success":
            return result
        elif result.status=="error": 
            return await self.handleError(result, None)
        else:
            return None

    async def handleError(self,error, client_error_message:Optional[str]):   
        if type(error) != Result:
            print("[ Exception Returned ]", error)
            return  Result().build("status","error").build("error",error).build("clientErrorMessage",client_error_message)
        else :
                print("[ Error Raised ]", error, client_error_message) 
                raise HTTPException(500, str(error.clientErrorMessage)) 
