from src.service.Service import Service
from src.model.User import User 
from src.util.HttpUtils import runner, runnerWithData
from typing import List, Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")
service = Service(User) 
router = APIRouter()

@router.get('/api/users', response_model=List[User]|None)
async def retrieve_users(token: Annotated[str, Depends(oauth2_scheme)]):
   async def setErrorMiddleware(result,data):
            result.build("status","error")
            result.build("error",{"error":"this is the error"})
            return result
   print("token ", token)
   return await runner(service.getAll,None)

@router.get('/api/users/{userid}/get/',response_model=User)
async def get_user(userid):
   async def setErrorMiddleware(result,data):
            result.build("status","error")
            result.build("error",{"error":"this is the error"})
            return result
   print("user id ",userid)
   return await runnerWithData(service.get,userid,None)

@router.post('/api/users/create')
async def create_user(user:User):
   return await runnerWithData(service.create,user,None)

@router.get('/api/users/delete/{userid}')
async def delete_user(userid):
    return await runnerWithData(service.delete,userid,None)  

@router.post('/api/users/update')
async def update_user(user:User):
   return await runnerWithData(service.update,user,None) 