# main.py
import uvicorn
import jwt
import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
import hashlib

# define app
app = FastAPI()
security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
timeLimit = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)

# env variable
TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
PASSWORD_SALT = os.getenv("PASSWORD_SALT")

# define CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# postgres connection
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST")
)
cursor = conn.cursor()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
def login(email: str, password: str):
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode('utf-8')).hexdigest()
    try:
        cursor.execute(
            "SELECT id,password FROM users where users.email = %s",
            (email,)
        )
        record = cursor.fetchone()
        if record != []:
            if record[1].strip() == password_hash:
                payload = {"user_id": record[0], "exp": timeLimit}
                token = jwt.encode(payload, TOKEN_SECRET_KEY)
                return {
                    "token": token,
                    "Elapse_time": f"{timeLimit}"
                }
            else:
                raise HTTPException(status_code=403, detail="You are not authorised")
        else:
            raise HTTPException(status_code=403, detail="You are not authorised")
    except:
        raise HTTPException(status_code=500, detail="An error has occurred")


@app.post("/register")
async def register(email: str, password: str, name: str, surname: str):
    password = hashlib.sha256((password + PASSWORD_SALT).encode('utf-8')).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO public.users(email, surname, name, password) VALUES (%s,%s,%s,%s) RETURNING public.users.id;",
            (email, surname, name, password)
        )
        conn.commit()
        payload = {"user_id": cursor.fetchone()[0], "exp": timeLimit}
        token = jwt.encode(payload, TOKEN_SECRET_KEY)
        return {
            "token": token,
            "Elapse_time": f"{timeLimit}"
        }
    except:
        raise HTTPException(status_code=500, detail="An error has occurred")


@app.get("/test")
async def test(token: str = Depends(oauth2_scheme)):
    if token:
        return jwt.decode(token, TOKEN_SECRET_KEY, algorithms=['HS256'])
    else:
        raise HTTPException(status_code=401, detail="An access token is required")
