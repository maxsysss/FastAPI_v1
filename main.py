from fastapi import FastAPI, Depends, HTTPException, status;
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
#API Based Authentication
from fastapi import Header;
API_KEY = "mysecureapikey";

#Session-Based Authentication
from fastapi import Request, Response, Form, Cookie;
from fastapi.responses import HTMLResponse, RedirectResponse;
import uuid;

#3.0 Simulate user and session store
fake_user_db = {"admin": "secret"};
session_store = {};



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

#3.1

@app.get("/login", response_class=HTMLResponse) #response_class=HTMLResponse para ele renderizar como página web, não como JSON
def login_form():
    return """
    <form action="/login" method="post">
        Username: <input name="username">
        Password: <input name="password" type="password">
        <input type="submit" value="Login">
        </form>
        """

@app.post("/login")
def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if fake_user_db.get(username) == password:
        session_id = str(uuid.uuid4())
        session_store[session_id] = username
        response = RedirectResponse(url="/dashboard", status_code=302) #encaminha para @app.get("/dashboard")
        response.set_cookie(key="session_id", value=session_id)
        return response;
    raise HTTPException(status_code=401, detail="Invalid login")

@app.get("/dashboard")
def dashboard(session_id: str = Cookie(None)):
    username = session_store.get(session_id)
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Welcome {username}!"}