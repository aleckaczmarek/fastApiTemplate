from fastapi import APIRouter, Depends 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from api.model.User import User
from api.model.Contract import Contract
from api.feature.user.UserUtils import  get_update_request_by_token, deny_if_user_exists, allow_access_by_user_id_or_admin

from system.transporters.Data import Data 
from system.transporters.Result import Result
from system.service.Service import Service
from system.util.HttpUtils import runner, runnerWithData 
from system.util.Routes import OAuth2PasswordBearer_Token_URL
from system.auth.Security import  get_password_hash, validate_token, get_current_active_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAuth2PasswordBearer_Token_URL)
service = Service(User())  
router = APIRouter()
auth_scheme = HTTPBearer()

# Ready
@router.get('/api/users', response_model=Result)
async def retrieve_users(token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials,["admin"],["admin:all"])
    return await runner(service.getAll,None)

# Needs end to end error handling confirmation, middleware works
@router.get('/api/users/get/{userid}',response_model=Result)
async def get_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)): 
    await validate_token(token.credentials)
    user = User(Id=userid)
    dataDTO = Data().build("data",user).build("options", {"token":token.credentials})
    print("data get ",dataDTO)
    return await runnerWithData(service.get,dataDTO,allow_access_by_user_id_or_admin)

# Needs end to end error handling confirmation
@router.post('/api/users/create',response_model=Result)
async def create_user(data:User,password:str):
    data.build("hashed_password",get_password_hash(password))
    dataDTO = Data()
    dataDTO.build("data", data)
    return await runnerWithData(service.create,dataDTO,deny_if_user_exists)

# Needs end to end error handling confirmation 
@router.get('/api/users/delete/{userid}')
async def delete_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    user = User(Id=userid)
    dataDTO = Data().build("data",user).build("options", {"token":token.credentials})
    return await runnerWithData(service.delete,dataDTO,allow_access_by_user_id_or_admin)  

# Needs adjustment, token validation, error handling, end to end 
#test
# Verify that update is corrupting db, determine why and resolve. I Think it isnt but tbd. Prob machine left on too long.
@router.post('/api/users/update',response_model=Result)
async def update_user(data:User, token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    user =  await get_current_active_user(token.credentials)
    dataDTO = Data()
    dataDTO.build("data", data)
    dataDTO.build("options", {"token":token.credentials})
    return  await runnerWithData(service.update,dataDTO,get_update_request_by_token)
     