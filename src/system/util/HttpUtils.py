from typing import Optional
from fastapi import HTTPException 

from system.transporters.Result import Result
from system.util.General import prettyPrint

async def runner(run,middleware):
    result =  await run(middleware)
    if result.status=="success":
        return result.build("middlewareData",{})
    elif result.status=="error":
        return await handleError(result, None)
    else:
        return None
    
async def runnerWithData(run,data,middleware):
    result =  await run(data,middleware) 
    if result.status=="success":
        return result.build("middlewareData",{})
    elif result.status=="error": 
        return await handleError(result, None)
    else:
        return None

async def returnErrorCheckResolver(result):
    if result is not None and type(result) is Result and result.status is "error":
        return True
    else:
        return False   

async def handleError(error, client_error_message:Optional[str | None] = None):   
    if type(error) != Result:
        print("[ Exception Returned ]")
        prettyPrint(error)
        res = Result().build("status","error").build("error",error)
        if client_error_message is not None:
            res.build("clientErrorMessage",client_error_message)
        return  res
    else :
            print("[ Error Raised ]") 
            prettyPrint(error)
            raise HTTPException(500, str(error.clientErrorMessage)) 
