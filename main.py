from fastapi import FastAPI, Depends, HTTPException, status;
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI();

security = HTTPBasic();

@app.get("/")
def read_root():
    return { "message": "Welcome to FastAPI Auth Tutorial"}

@app.get("/basic-auth")
def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin") #secrets.compare_digest() para comparação segura de strings (prevenção de "timming attacks")
    correct_password = secrets.compare_digest(credentials.password, "secret")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate":"Basic"},
        )
    return {"message": f"Welcome {credentials.username}"}