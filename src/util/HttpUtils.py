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
    print("runnerWithData result ",result)
    if result.status=="success":
        return result
    elif result.status=="error":
        print("error raised in runnerwith data")
        raise result.error
    else:
        return None
    

async def handleError(error, status, message):
   if type(error) == HTTPException: 
        raise error
   else:
        raise HTTPException(status,message)