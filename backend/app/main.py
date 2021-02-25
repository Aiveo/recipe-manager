# main.py
import uvicorn
import json
import jwt
import datetime
from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel

class Login(BaseModel):
    email: str
    password: str

app = FastAPI()
SECRET_KEY = "hkBxrbZ9Td4QEwgRewV6gZSVH4q78vBia4GBYuqd09SsiMsIjH"

conn = psycopg2.connect(dbname="RecipeManagerDB", user="RecipeManager", password="RecipeManagerPaSS", host="localhost")
cur = conn.cursor()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(login: Login):
    try:
        cur.execute(f"SELECT id,password FROM users where users.email = '{login.email}'")
        records = cur.fetchall()
        if records[0][1].strip() == login.password:
            timeLimit = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            payload = {"user_id": records[0][0], "exp": timeLimit}
            token = jwt.encode(payload, SECRET_KEY)
            return_data = {
                "error": "0",
                "message": "Successful",
                "token": token,
                "Elapse_time": f"{timeLimit}"
            }
        else:
            return_data = {
                "error": "1",
                "message": "Bad Username or Password"
            }
    except:
        return_data = {
            "error": "2",
            "message": "Error occured",
        }
    return return_data


@app.get("/test/{token}")
async def test(token):
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
