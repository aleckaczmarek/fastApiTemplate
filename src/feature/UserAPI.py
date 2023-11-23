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

@router.get('/api/users', response_model=Result)
async def retrieve_users(token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials  )
    return await runner(service.getAll,None)

@router.get('/api/users/get/{userid}',response_model=Result)
async def get_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)): 
    print("token ",token)
    print("userid ",userid)
    await validate_token(token.credentials, ) 
    #TODO add middleware to filter out access say if token user 
    # id does not match user id and group admin does not exist etc
    # any user can get any user currently
    user = User().build("Id",userid)
    data = Data().build("data",user)
    print("data get ",data)
    return await runnerWithData(service.get,data,None)

@router.post('/api/users/create',response_model=Result)
async def create_user(data:Data,password:str):
    async def denyIfUserExists(result, data):
        user = await get_user_security(data.data.username) 
        if user :
            print("user found ", user)
            result.build("status","error")
            result.build("clientErrorMessage", "Invalid username.")
            result.build("error","Invalid username.")
            return result
        else: 
            totalusers = await runner(service.getAll,None) 
            data.data.build("Id",str(len(totalusers.data.get("query"))))
            result.build("data",data.data)
            result.build("status","success")
            return result
    userToCreate= User(**data.data.dict())
    userToCreate.build("hashed_password",get_password_hash(password))
    data.build("data",userToCreate)
    return await runnerWithData(service.create,data,denyIfUserExists)
# TODO currently not working, needs fixing post data struc change
@router.get('/api/users/delete/{userid}')
async def delete_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    #TODO add middleware to filter out access say if token user 
    # id does not match user id and group admin does not exist etc
    # any user can delete any user currently
    return await runnerWithData(service.delete,userid,None)  

@router.post('/api/users/update',response_model=Result)
async def update_user(data:Data, token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    async def getUserIdByToken(result, data):
        print("in middleware of declaration",data)
        user = await get_current_user(data.options.get("token"))
        if(data.data.Id != user.Id):
            print("[ ERROR ] IDS DO NOT MATCH")
            return result.build("data",{}).build("status","error").build("error","IDS DO NOT MATCH")
        print("type of user ", type(user))
        user_update_req = data.data
        user_update_req.build("Id", user.Id)
        user_update_req.build("full_name", user.first_name+" "+user.last_name)
        #Prevent password update
        user_update_req.build("hashed_password",None)
        #Prevent admin update
        user_update_req.build("auths",None)
        #Prevent groups update
        user_update_req.build("groups",None)
        result.build("data",user_update_req)
        result.build("status","success")
        return result
    await validate_token(token.credentials)
    print("[ Data ]",data)
    data.build("options", {**data.options, "token":token.credentials})
    return  await runnerWithData(service.update,data,getUserIdByToken)
     