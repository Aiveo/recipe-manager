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
async def register(email: str, password: str, lastname: str, firstname: str):
    password = hashlib.sha256((password + PASSWORD_SALT).encode('utf-8')).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO public.users(email, firstname, lastname, password) VALUES (%s,%s,%s,%s) RETURNING public.users.id;",
            (email, lastname, firstname, password)
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


@app.get("/getRecipes")
async def getRecipes():
    recipes = []
    sql = "SELECT id,name,description,picture FROM public.recipes;"
    try:
        cursor.execute(sql)
        for recipe in cursor.fetchall():
            recipes.append({
                "id": recipe[0],
                "name": recipe[1].strip(),
                "description": recipe[2],
                "image": recipe[3]
            })
        return recipes
    except:
        raise HTTPException(status_code=500, detail="An error has occurred")


@app.get("/getOneRecipe")
async def getOneRecipe(id: int):
    sql = """SELECT 
                public.recipes.id, 
                public.recipes.name, 
                public.recipes.preparation_time, 
                public.recipes.cooking_time, 
                public.recipes.description, 
                public.recipes.picture, 
                public.recipes.portion, 
                public.users.id, 
                public.users.firstname, 
                public.users.lastname
            FROM public.recipes
            INNER JOIN public.users
            ON public.recipes.id_ref_user = public.users.id
            WHERE public.recipes.id = %s;"""
    sql2 = """SELECT step
            FROM recipe_steps
            WHERE id_ref_recipe = %s
            ORDER BY step_order;"""
    sql3 = """SELECT
                public.recipe_ingredients.quantity,
                public.measurement_unit.name,
                public.ingredients.name
            FROM
            (
                public.recipe_ingredients
                INNER JOIN public.ingredients
                ON public.recipe_ingredients.id_ref_ingredient = public.ingredients.id
            )
            INNER JOIN public.measurement_unit
            ON public.recipe_ingredients.id_ref_measurement_unit = public.measurement_unit.id
            WHERE public.recipe_ingredients.id_ref_recipe = %s;"""
    try:
        cursor.execute(sql, (id,))
        recipe = cursor.fetchone()
        recipe = {
            "id": recipe[0],
            "name": recipe[1].strip(),
            "preparation_time": recipe[2],
            "cooking_time": recipe[3],
            "description": recipe[4],
            "image": recipe[5],
            "portion": recipe[6],
            "id_user": recipe[7],
            "firstname": recipe[8].strip(),
            "lastname": recipe[9].strip()
        }
        cursor.execute(sql2, (id,))
        steps = cursor.fetchall()
        recipe["steps"] = steps

        cursor.execute(sql3, (id,))
        ingredients = []
        for ingredient in cursor.fetchall():
            ingredients.append(str(ingredient[0]) + " " + str(ingredient[1]).strip() + " de " + str(ingredient[2]).strip())
        recipe['ingredients'] = ingredients
        return recipe
    except:
        raise HTTPException(status_code=500, detail="An error has occurred")