from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from . import utils, schemas
from .routers import posts, users

app = FastAPI()




# creating a connection with my pg admmin
try:
    conn = psycopg2.connect(host='localhost', database='api_py', user='postgres', password='united1234',
    cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was succesful!')
except Exception as error:
    print('Connection to database failed')
    print('Error: ', error)

# my hard coded content body
my_posts = [{
    "Name" : "Ayo", "Job" : "Software Developer", "Native" : "Yoruba", "Learnt" : "Francais", "id" : 1}, {
    "Name" : "Bami", "Job" : "Cloud Engineer", "Native" : "Yoruba", "Learnt" : "Spanish", "id" : 2
}]

# function for post request
def find_post(id):
   for p in my_posts:
      if p["id"] == id:
        return p

# function for delete request
def post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#including router after cleaning up my code  
app.include_router(posts.router)
app.include_router(users.router) 
 
#get method using root ('/')
@app.get("/")
def root():
    return {'reponse' : 'Salut World'}



