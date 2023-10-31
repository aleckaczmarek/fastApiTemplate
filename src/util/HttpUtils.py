from fastapi import HTTPException

async def runner(run,middleware):
    result =  await run(middleware)
    if result.status=="success":
        return result.data
    elif result.status=="error":
        raise HTTPException(status_code=404, detail=result.error)
    else:
        return None
    
async def runnerWithData(run,data,middleware):
    result =  await run(data,middleware)
    if result.status=="success":
        return result.data
    elif result.status=="error":
        raise HTTPException(status_code=500, detail=result.error)
    else:
        return None
    