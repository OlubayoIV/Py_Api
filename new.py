from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Posts(BaseModel):
    Name: str
    Job: str
    
#get method using root ('/')
@app.get("/")
async def testing():
    return {'reponse' : 'Salut World'}

#get method using root ('/comment')
@app.get("/comments")
def get_comments():
    return {'data' : 'votre reponse est ici'}

#post method
@app.post("/createposts")
def create_comments(post: Posts):
    print(post)
    return {"mon reponse" : "nouvel"}