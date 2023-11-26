from fastapi import HTTPException  

from api.model.User import User
 
from system.service.Service import Service
from system.util.HttpUtils import HttpUtils 
from system.auth.Security import get_user_security, get_current_user


service = Service(User)  
httpUtils = HttpUtils()

runner = httpUtils.runner


async def get_update_request_by_token(result, data):
        print("in middleware of declaration",data)
        user = await get_current_user(data.options.get("token"))
        if(data.data.Id != user.Id): 
            return result.build("data",{}).build("status","error").build("error","IDS DO NOT MATCH").build("clientErrorMessage","Access Denied")
        print("type of user ", type(user))
        user_update_req = data.data
        user_update_req.build("Id", user.Id)
        user_update_req.build("full_name", user.first_name+" "+user.last_name)
        if user_update_req.first_name is not None and user_update_req.last_name is not None:
            user_update_req.build("full_name", user_update_req.first_name+" "+user_update_req.last_name)
        if user_update_req.first_name is not None and user_update_req.last_name is not None:
            user_update_req.build("full_name", user_update_req.first_name+" "+user_update_req.last_name)
        if user_update_req.first_name is not None and user_update_req.last_name is  None:
            user_update_req.build("full_name", user_update_req.first_name+" "+user.last_name)
        if user_update_req.first_name is  None and user_update_req.last_name is not None:
            user_update_req.build("full_name", user.first_name+" "+user_update_req.last_name)
        #Prevent password update
        user_update_req.build("hashed_password",None)
        #Prevent admin update
        user_update_req.build("auths",None)
        #Prevent groups update
        user_update_req.build("groups",None)
        result.build("data",user_update_req)
        result.build("status","success")
        return result
    

async def set_error_middleware(result,data):
    raise HTTPException(400,"denied from middleware")


async def deny_if_user_exists(result, data):
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