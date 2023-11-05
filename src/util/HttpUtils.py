from fastapi import HTTPException

async def runner(run,middleware):
    result =  await run(middleware)
    if result.status=="success":
        return result
    elif result.status=="error":
        raise HTTPException(status_code=404, detail=result.error)
    else:
        return None
    
async def runnerWithData(run,data,middleware):
    result =  await run(data,middleware) 
    if result.status=="success":
        return result
    elif result.status=="error": 
        await handleError(result, 500, "Error in runnerWithData response") 
    else:
        return None
    

async def handleError(error_to_examine, status, message):  
   if type(error_to_examine) == HTTPException:  
        raise error_to_examine
   else: 
        if (type(error_to_examine.error)==str):
            raise HTTPException(status, error_to_examine.error)
        else :
            raise HTTPException(status, message)