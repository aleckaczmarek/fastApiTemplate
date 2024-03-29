from fastapi import HTTPException  

from api.model.User import User
 
from system.service.Service import Service 
from system.util.HttpUtils import returnErrorCheckResolver, runner 
from system.auth.Security import get_user_security, get_current_user, validate_by_auth_and_group

service = Service(User())  
 

async def get_update_request_by_token(result, data):
    print("in middleware of declaration",data)
    user = await get_current_user(data.options.get("token"))
    await allow_access_by_user_id_or_admin(result,data)
    
    print("type of user ", type(user))
    print(" get_update_request_by_token gotten  user ", user)
    # TODO verify still works after adding get_new_instance method 
    # TODO determine better way to assign id, if admin makes request wrong id would be assigned
    user_update_req = data.data.get_new_instance(**{**data.data.dict(),"Id":user.Id})
    # user_update_req.build("Id", user.Id)
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


async def allow_access_by_user_id_or_admin(result, data): 
    print("token inside allow_access_by_user_id_or_admin", data.options.get("token"))
    user = await get_current_user(data.options.get("token")) 
    if await returnErrorCheckResolver(user):
        return user
    print("allow_access_by_user_id_or_admin user gotten ", user)
    auths:list[str] = user.auths
    groups:list[str] = user.groups
    groups = ' '.join(str(g)for g in groups)
    auths = ' '.join(str(a)for a in auths)
    print("about to validate by auth angr group")
    try:
        if data.data.Id is not user.Id and validate_by_auth_and_group(auths,groups,["admin"],["admin:all", "admin:read", "admin:write", "admin:update"]) is not True  : 
            print("[ REJECTED ALLOW ACCESS BY USER ID OR ADMIN ] ")
            return result.build("data",{}).build("status","error").build("error","IDS DO NOT MATCH").build("clientErrorMessage","Access Denied")
    except HTTPException  as error:
        print("[ ALLOW ACCESS BY USER ID OR ADMIN DENIED]",error)
        return result.build("data",{}).build("status","error").build("error","IDS DO NOT MATCH").build("clientErrorMessage","Access Denied")
    
    result.build("data",data.data)
    result.build("status","success")
    print("result ", result)
    print("BUILDING RESULT allow_access_by_user_id_or_admin ",data )
    return result

async def set_error_middleware(result,data):
    raise HTTPException(400,"denied from middleware")


async def deny_if_user_exists(result, data):
        print("deny now")
        user = await get_user_security(data.data.username)  
        if type(user) is User :
            print("user found ", user)
            result.build("status","error")
            result.build("clientErrorMessage", "Invalid username.")
            result.build("error","Invalid username.")
            return result
        else: 
            totalusers = await runner(service.getAll,None) 
            users = totalusers.data.get("query")
            next_id = len(users)
            dict = data.data.dict()
            dict['Id'] = str(next_id)
            result.build("data",User(**dict))
            result.build("status","success")
            return result