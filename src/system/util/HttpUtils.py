from typing import Optional
from fastapi import HTTPException 

from system.transporters.Result import Result
from system.util.General import prettyPrint

async def runner(run,middleware):
    result =  await run(middleware)
    print("result in http utils ", result)
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

async def returnErrorCheckResolver(result):
    if result is not None and type(result) is Result and result.status is "error":
        return True
    else:
        return False   

async def handleError(error, client_error_message:Optional[str]):   
    if type(error) != Result:
        print("[ Exception Returned ]")
        prettyPrint(error)
        return  Result().build("status","error").build("error",error).build("clientErrorMessage",client_error_message)
    else :
            print("[ Error Raised ]") 
            prettyPrint(error)
            raise HTTPException(500, str(error.clientErrorMessage)) 
