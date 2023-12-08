from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import   OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import JWTError, jwt 
from passlib.context import CryptContext
from pydantic import BaseModel

from api.model.User import User 

from system.service.Service import Service
from system.util.Routes import Routes 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Routes.OAuth2PasswordBearer_Token_URL) 
router = APIRouter()
user_service = Service(User) 
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_security(username: str):
    response = None 
    response = await user_service.getWhere("username",username,None)
    print("respone in get user", response)
    if len(response) == 0:
        return None
    user =  User(**response[0].dict())
    print("userc reated ",user) 
    return user

async def authenticate_user(username: str, password: str): 
    user = await get_user_security(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    print("auth user")
    user.build("hashed_password",None)
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"iat":datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]): 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print("username from jwt payload.geta ",username)
        print("token data ",token_data)
    except JWTError:
        raise credentials_exception
    user = await get_user_security(username=token_data.username) 
    if user is None:
        raise credentials_exception
    return user 

def get_token(header):
    if(header == None):
        raise credentials_exception
    bearer, _, token = header.partition(' ')
    if bearer.lower() != 'bearer':
        raise credentials_exception
    return token

def validate_by_auth_and_group(auths:Optional[list[str]]=None,groups:Optional[list[str]]=None,allowed_auths:Optional[list[str]]=None,allowed_groups:Optional[list[str]]=None):
    print("[ START VALIDATE BY AUTH AND GROUP ]")
    accessAuth = False
    accessGroup = False
    if allowed_groups is None:
        accessGroup = True
    if allowed_auths is None:
        accessAuth = True
    if type(allowed_auths) is not list and type(allowed_auths) is not type(None):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Allowed Auths and allowed Groups must be inserted as list[str] type",
                headers={"WWW-Authenticate": "Bearer"},
            )
    if type(allowed_groups) is not list and type(allowed_groups) is not type(None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= "Allowed Auths and allowed Groups must be inserted as list[str] type",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    while accessAuth is False:
        if  allowed_auths is not None:
            for auth in allowed_auths:
                print("auth ", auth)
                if auth is not None and auths is not None and auth in auths :
                    accessAuth = True 
            if accessAuth is False:
                raise credentials_exception
    while accessGroup is False: 
        if  allowed_groups is not None:
            for group in allowed_groups:
                print("group ", group)
                if group is not None and groups is not None and group in groups :
                    accessGroup = True 
            if accessGroup is False:
                raise credentials_exception
        if accessGroup and accessAuth is False:
            raise credentials_exception
    print("[ END VALIDATE BY AUTH AND GROUP ] TRUE AUTHORIZED")
    return True

async def validate_token(token: Annotated[str, Depends(oauth2_scheme)],allowed_auths:Optional[list[str]]=None,allowed_groups:Optional[list[str]]=None):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        auths:list[str] = payload.get("auths")
        groups:list[str] = payload.get("groups")
        groups = ' '.join(str(g)for g in groups)
        auths = ' '.join(str(a)for a in auths)

        if username is None:
            raise credentials_exception
        
        validate_by_auth_and_group(auths,groups,allowed_auths,allowed_groups)

        print("[ Authorized ]",{"valid":True})
        return {"valid":True}
    except JWTError  as error:
        print("[ Authorized ]",{"valid":False})
        raise credentials_exception

async def get_current_active_user(
     token: Annotated[str, Depends(oauth2_scheme)]
):
    current_user = await get_current_user(token)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/api/users/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(form_data.username, form_data.password) 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "auths":user.auths, "groups":user.groups, "email":user.email}, expires_delta=access_token_expires
    )
    # TODO add cookie response here for session 
    return {"access_token":access_token,"token_type":"bearer"}

@router.get("/api/users/me/", response_model=User)
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    user = await get_current_active_user(token)
    print("user from get ", user)
    user.build("hashed_password",None)
    return user
