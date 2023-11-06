from typing import Optional
from fastapi import HTTPException

from src.model.Result import Result

async def runner(run,middleware):
    result =  await run(middleware)
    if result.status=="success":
        return result
    elif result.status=="error":
        return await handleError(result, None)
    else:
        return None
    
async def runnerWithData(run,data,middleware):
    result =  await run(data,middleware) 
    if result.status=="success":
        return result
    elif result.status=="error": 
        return await handleError(result, None)
    else:
        return None
    

async def handleError(error, client_error_message:Optional[str]):   
   print("error ", error)
   if type(error) != Result:
       print("build error ", error)
       return  Result().build("status","error").build("error",error).build("clientErrorMessage",client_error_message)
   else :
        print("[ Error Raised ]", error) 
        raise HTTPException(500, str(error.clientErrorMessage)) 
