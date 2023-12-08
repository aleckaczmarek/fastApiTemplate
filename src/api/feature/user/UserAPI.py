from fastapi import APIRouter, Depends 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from api.model.User import User
from api.feature.user.UserUtils import  get_update_request_by_token, deny_if_user_exists, allow_access_by_user_id_or_admin

from system.transporters.Data import Data 
from system.transporters.Result import Result
from system.service.Service import Service
from system.util.HttpUtils import HttpUtils 
from system.util.Routes import Routes 
from system.auth.Security import  get_password_hash, validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Routes.OAuth2PasswordBearer_Token_URL)
service = Service(User)  
router = APIRouter()
auth_scheme = HTTPBearer()
httpUtils = HttpUtils()

runner = httpUtils.runner
runnerWithData = httpUtils.runnerWithData

# Ready
@router.get('/api/users', response_model=Result)
async def retrieve_users(token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials,["admin"],["admin:all"])
    return await runner(service.getAll,None)

# Needs end to end error handling confirmation
@router.get('/api/users/get/{userid}',response_model=Result)
async def get_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)): 
    print("token ",token)
    print("userid ",userid)
    await validate_token(token.credentials) 
    #TODO add middleware to filter out access say if token user 
    # id does not match user id and group admin does not exist etc
    # any user can get any user currently
  
    user = User().build("Id",userid) 
    data = Data().build("data",user).build("options", {"token":token.credentials})
    print("data get ",data)
    return await runnerWithData(service.get,data,allow_access_by_user_id_or_admin)

# Needs end to end error handling confirmation
@router.post('/api/users/create',response_model=Result)
async def create_user(data:Data,password:str):
    userToCreate= User(**data.data.dict())
    userToCreate.build("hashed_password",get_password_hash(password))
    data.build("data",userToCreate)
    return await runnerWithData(service.create,data,deny_if_user_exists)

# Needs end to end error handling confirmation
# TODO currently not working, needs fixing post data struc change
@router.get('/api/users/delete/{userid}')
async def delete_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    #TODO add middleware to filter out access say if token user 
    # id does not match user id and group admin does not exist etc
    # any user can delete any user currently
    return await runnerWithData(service.delete,userid,None)  

# Needs adjustment, token validation, error handling, end to end 
#test
@router.post('/api/users/update',response_model=Result)
async def update_user(data:Data, token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials)
    print("[ Data ]",data)
    data.build("options", {**data.options, "token":token.credentials})
    return  await runnerWithData(service.update,data,get_update_request_by_token)
     