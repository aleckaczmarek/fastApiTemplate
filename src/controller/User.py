from src.model.Result import Result
from src.service.Service import Service
from src.auth.Security import get_password_hash, validate_token
from src.model.User import User  
from src.util.HttpUtils import runner, runnerWithData
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from src.util.Routes import Routes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Routes.OAuth2PasswordBearer_Token_URL)
service = Service(User) 
router = APIRouter()
auth_scheme = HTTPBearer()
async def setErrorMiddleware(result,data):
            # result.build("status","error")
            # result.build("error","this is the error from middle ware ")
            raise HTTPException(400,"denied from middleware")
            # return result 
@router.get('/api/users', response_model=List[User]|None)
async def retrieve_users( token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
   is_authenticated = await validate_token(token.credentials, "user" ,"user:self" )
   print("is auth ",is_authenticated)
   return await runner(service.getAll,None)

@router.get('/api/users/{userid}/get/',response_model=User)
async def get_user(userid):
   print("user id ",userid)
   return await runnerWithData(service.get,userid,None)

@router.post('/api/users/create')
async def create_user(user:User,password:str):
   print("Starting ")
   userToCreate= User(**user.dict())
   print("created, ", userToCreate)
   print("password ",password)
   hashedPassword = get_password_hash(password)
   userToCreate.build("hashed_password",hashedPassword)
   return await runnerWithData(service.create,userToCreate,None)

@router.get('/api/users/delete/{userid}')
async def delete_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    return await runnerWithData(service.delete,userid,None)  

@router.post('/api/users/update',response_model=Result)
async def update_user(user:User, token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
   is_authenticated = await validate_token(token.credentials)
   print("is auth ",is_authenticated)
   print("user ",user)
   return await runnerWithData(service.update,user,None) 