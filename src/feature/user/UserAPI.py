from fastapi import APIRouter, Depends 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from src.transporters.Data import Data 
from src.transporters.Result import Result
from src.service.Service import Service
from src.util.HttpUtils import HttpUtils 
from src.util.Routes import Routes 
from src.model.User import User

from src.auth.Security import  get_password_hash, validate_token
from src.feature.user.UserUtils import  get_update_request_by_token, deny_if_user_exists, set_error_middleware


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Routes.OAuth2PasswordBearer_Token_URL)
service = Service(User)  
router = APIRouter()
auth_scheme = HTTPBearer()
httpUtils = HttpUtils()

runner = httpUtils.runner
runnerWithData = httpUtils.runnerWithData


@router.get('/api/users', response_model=Result)
async def retrieve_users(token:HTTPAuthorizationCredentials = Depends(auth_scheme)):
    await validate_token(token.credentials  )
    return await runner(service.getAll,None)

@router.get('/api/users/get/{userid}',response_model=Result)
async def get_user(userid,token:HTTPAuthorizationCredentials = Depends(auth_scheme)): 
    print("token ",token)
    print("userid ",userid)
    await validate_token(token.credentials) 
    #TODO add middleware to filter out access say if token user 
    # id does not match user id and group admin does not exist etc
    # any user can get any user currently
    user = User().build("Id",userid)
    data = Data().build("data",user)
    print("data get ",data)
    return await runnerWithData(service.get,data,None)

@router.post('/api/users/create',response_model=Result)
async def create_user(data:Data,password:str):
    userToCreate= User(**data.data.dict())
    userToCreate.build("hashed_password",get_password_hash(password))
    data.build("data",userToCreate)
    return await runnerWithData(service.create,data,deny_if_user_exists)
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
    await validate_token(token.credentials)
    print("[ Data ]",data)
    data.build("options", {**data.options, "token":token.credentials})
    return  await runnerWithData(service.update,data,get_update_request_by_token)
     