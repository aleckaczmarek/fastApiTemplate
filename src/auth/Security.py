from datetime import datetime, timedelta
from typing import Annotated, List, Optional

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 

from jose import JWTError, jwt 
from passlib.context import CryptContext
from pydantic import BaseModel
from src.model.User import User 
from src.service.Service import Service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")
router = APIRouter()
user_service = Service(User)
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

async def get_user(username: str):
    response = await user_service.getWhere("username",username,None)
    return User(**response.data[0].dict())

async def authenticate_user(username: str, password: str): 
    user = await get_user(username) 
    print("user in db return ", user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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
    user = await get_user(username=token_data.username) 
    if user is None:
        raise credentials_exception
    return user

async def validate_token(token: Annotated[str, Depends(oauth2_scheme)],allowed_auth:Optional[str]=None,allowed_groups:Optional[str]=None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        auth:str = payload.get("auth")
        groups:List[str] = payload.get("groups")
        groups = ' '.join(str(g)for g in groups)
        if username is None:
            raise credentials_exception
        if allowed_auth is not None and auth is not None and auth not in allowed_auth :
            raise credentials_exception
        if allowed_groups is not None and groups is not None and groups not in allowed_groups :
            raise credentials_exception

        token_data = TokenData(username=username)
        print("username from jwt payload.geta ",username)
        print("token data ",token_data)
        return {"valid":True}
    except JWTError:
        raise credentials_exception

async def get_current_active_user(
     token: Annotated[str, Depends(oauth2_scheme)]
):
    current_user = await get_current_user(token)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/api/users/token", response_model=Token)
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
        data={"sub": user.username, "auth":user.auth, "groups":user.groups, "email":user.email}, expires_delta=access_token_expires
    )
    return {"access_token":access_token,"token_type":"bearer"}

@router.get("/api/users/me/", response_model=User)
async def read_users_me(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    user = await get_current_active_user(token)
    print("user from get ", user)
    return user

@router.get("/api/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]