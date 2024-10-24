from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from google.oauth2 import id_token
from google.auth.transport import requests
from typing import Optional
import os

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get("GOOGLE_CLIENT_ID"))
        userid = idinfo['sub']
        return userid
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real application, you would verify the credentials against a database
    # and issue a token.  For this example, we'll just return a dummy token.
    return {"access_token": "dummy_token", "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"user_id": current_user}

