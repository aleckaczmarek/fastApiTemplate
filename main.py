import uvicorn
from fastapi import FastAPI 
from src.controller import User

app = FastAPI()
app.include_router(User.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True,
                timeout_keep_alive=3600, workers=10)
