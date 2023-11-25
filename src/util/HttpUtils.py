from typing import Optional
from fastapi import HTTPException 
from src.transporters.Result import Result
from src.util.General import General

class HttpUtils():
    def __init__(self): 
        self.generalUtils = General()
    async def runner(self,run,middleware):
        result =  await run(middleware)
        print("result in http utils ", result)
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
            print("[ Exception Returned ]")
            self.generalUtils.prettyPrint(error)
            return  Result().build("status","error").build("error",error).build("clientErrorMessage",client_error_message)
        else :
                print("[ Error Raised ]") 
                self.generalUtils.prettyPrint(error)
                self.generalUtils.prettyPrint(error.error)
                self.generalUtils.prettyPrint(error.clientErrorMessage)
                raise HTTPException(500, str(error.clientErrorMessage)) 
