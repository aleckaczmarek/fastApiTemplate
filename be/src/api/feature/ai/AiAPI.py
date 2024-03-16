from fastapi import APIRouter, Depends 
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from api.model.AiModel import AiModel
 
from system.transporters.Result import Result 
from system.util.HttpUtils import runner 
from system.util.AiConnect import AiConnect
from system.util.Routes import OAuth2PasswordBearer_Token_URL
from system.auth.Security import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAuth2PasswordBearer_Token_URL)
router = APIRouter()
auth_scheme = HTTPBearer()  

@router.post('/api/ai/ask',response_model=Result)
async def ask_ai_post(data:AiModel):
    question = data.question
    print("INSIDE POST REQ ", data)
    ai = AiConnect("llama2")  
    chat = await ai.getResponse(question)
    return Result().build("data",chat)


@router.post('/api/ai/ask/{ollama_llm_name}',response_model=Result)
async def ask_ai_post(data:AiModel,ollama_llm_name):
    question = data.question
    print("INSIDE POST REQ ", data)
    ai = AiConnect(ollama_llm_name)  
    chat = await ai.getResponse(question)
    return Result().build("data",chat)
 