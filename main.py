from fastapi import FastAPI, Depends, HTTPException, status;
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import Header;

API_KEY = "mysecureapikey";

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

@app.get("/apikey-auth")
def apikey_auth(x_api_key: str = Header(...)): #Header(...) é uma função do FastAPI usada para extrair valores dos cabeçalhos HTTP da requisição
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401, detail="Invalid API Key"
        )
    return {"message": "API Key authenticated!"}