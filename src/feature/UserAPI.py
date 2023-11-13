from fastapi import APIRouter, Depends, HTTPException 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from typing import List
from src.transporters.Data import Data
from src.auth.Security import get_user_security
from src.transporters.Result import Result
from src.service.Service import Service
from src.auth.Security import get_current_user, get_password_hash, validate_token
from src.util.HttpUtils import HttpUtils 
from src.util.Routes import Routes 
from src.model.User import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Routes.OAuth2PasswordBearer_Token_URL)
service = Service(User)  
router = APIRouter()
auth_scheme = HTTPBearer()
httpUtils = HttpUtils()
runner = httpUtils.runner
runnerWithData = httpUtils.runnerWithData

   
async def setErrorMiddleware(result,data):
    raise HTTPException(400,"denied from middleware")

@router.get('/api/users', response_model=List[User]|None)
async def retrieve_users( token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    is_authenticated = await validate_token(token.credentials, "user" ,"user:self" )
    print("is auth ",is_authenticated)
    return await runner(service.getAll,None)

@router.get('/api/users/{userid}/get/',response_model=User)
async def get_user(userid):
    print("user id ",userid)
    return await runnerWithData(service.get,userid,None)

@router.post('/api/users/create',response_model=Result)
async def create_user(data:Data,password:str):
    async def denyIfUserExists(result, data):
        print("user deny middleware ",data)
        user = await get_user_security(data.data.username)
        print("user here ", type(user))
        if user :
            print("user found ", user)
            result.build("status","error")
            result.build("clientErrorMessage", "Invalid username.")
            result.build("error","Invalid username.")
            return result
        else:
            print("user not found ")
            result.build("data",data.data)
            result.build("status","success")
            return result
    print("Starting ")
    userToCreate= User(**data.data.dict())
    print("created, ", userToCreate)
    print("password ",password)
    hashedPassword = get_password_hash(password)
    userToCreate.build("hashed_password",hashedPassword)
    data.build("data",userToCreate)
    return await runnerWithData(service.create,data,denyIfUserExists)

@router.get('/api/users/delete/{userid}')
async def delete_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    return await runnerWithData(service.delete,userid,None)  

@router.post('/api/users/update',response_model=Result)
async def update_user(data:Data, token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    async def getUserIdByToken(result, data):
        print("in middleware of declaration",data.options)
        user = await get_current_user(data.options.get("token"))
        print("type of user ", type(user))
        user_update_req = data.data
        user_update_req.build("Id", user.Id)
        #Prevent password update
        user_update_req.build("hashed_password",None)
        #Prevent admin update
        user_update_req.build("auth",None)
        #Prevent groups update
        user_update_req.build("groups",None)
        result.build("data",user_update_req)
        result.build("status","success")
        return result
    
    is_authenticated = await validate_token(token.credentials)
    print("[ User Authorized ] ",is_authenticated)
    print("[ Data ]",data)
    data.build("options", {**data.options, "token":token.credentials})
    return  await runnerWithData(service.update,data,getUserIdByToken)
     