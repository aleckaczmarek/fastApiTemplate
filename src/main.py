import uvicorn
from fastapi import FastAPI 

from api.feature.ai.AiAPI import router as ai_router
from api.feature.user.UserAPI import router as user_router
from system.auth.Security import router as security_router

app = FastAPI()
app.include_router(ai_router)
app.include_router(user_router)
app.include_router(security_router)
 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True,
                timeout_keep_alive=3600, workers=10)
