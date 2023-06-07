from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    Name: str
    Job: str
    rating: Optional[int] = None
    
my_posts = [{
    "Name" : "Ayo", "Job" : "Software Developer", "Native" : "Yoruba", "Learnt" : "Francais", "id" : 1}, {
    "Name" : "Bami", "Job" : "Cloud Engineer", "Native" : "Yoruba", "Learnt" : "Spanish", "id" : 2
}]

def find_post(id):
   for p in my_posts:
      if p["id"] == id:
        return p

#get method using root ('/')
@app.get("/")
def root():
    return {'reponse' : 'Salut World'}

#get method using root ('/comment')
@app.get("/posts")
def get_comments():
    return {'data' : my_posts}

#post method 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_comments(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"mon reponse" : post_dict}

# getting specific post using id
@app.get('/posts/{id}')
def get_specific_comment(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id : {id} was not found')
    return {"la detail" : post}