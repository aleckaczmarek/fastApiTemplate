from fastapi import APIRouter, Depends 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
 
from system.transporters.Result import Result 
from system.util.HttpUtils import runner 
from system.util.AiConnect import AiConnect
from system.util.Routes import OAuth2PasswordBearer_Token_URL
from system.auth.Security import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAuth2PasswordBearer_Token_URL)
ai = AiConnect("llama2")  
router = APIRouter()
auth_scheme = HTTPBearer()  
# ask_ai(token:HTTPAuthorizationCredentials = Depends(auth_scheme))
# Ready
@router.get('/api/ai/ask/{question}', response_model=Result)
async def ask_ai(question):
    # await validate_token(token.credentials,["admin"],["admin:all"])
    chat = await ai.getResponse(question)
    return Result().build("data",chat)
 