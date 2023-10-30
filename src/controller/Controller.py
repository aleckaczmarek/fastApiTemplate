import uvicorn
from fastapi import FastAPI, HTTPException
from src.service.Service import Service
from src.model.User import User 
from typing import List

class Controller():
    def __init__(self, model,app):
        self.model = model
        self.app = app
        self.collection_name = model().collection_name
        self.service = Service(model)

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
        
    # self.app.get('/api/${self.collection_name}', response_model=List[self.model]|None)
    async def retrieveAll(self):
        async def setErrorMiddleware(result,data):
                result.build("status","error")
                result.build("error",{"error":"this is the error"})
                return result
        return await self.runner(self.service.getAll,None)
     



@app.get('/api/users/{userid}',response_model=User)
async def get(userid):
   async def setErrorMiddleware(result,data):
            result.build("status","error")
            result.build("error",{"error":"this is the error"})
            return result
   print("user id ",userid)
   return await runnerWithData(self.service.get,userid,None)

@app.post('/api/users/create')
async def create_user(user:User):
   return await runnerWithData(self.service.create,user,None)

@app.get('/api/users/delete/{userid}')
async def delete_user(userid):
    return await runnerWithData(self.service.delete,userid,None)  

@app.post('/api/users/update')
async def update_user(user:User):
   return await runnerWithData(self.service.update,user,None) 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True,
                timeout_keep_alive=3600, workers=10)
