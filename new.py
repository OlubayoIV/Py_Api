from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Posts(BaseModel):
    Name: str
    Job: str
    
my_posts = [{
    "Name" : "Ayo", "Job" : "Software Developer", "Communication" : "Languages spoken", "Native" : "Yoruba", "Studied with" : "English", "Learnt" : "Francais", "id" : 1}, {
    "Name" : "Bami", "Job" : "Cloud Engineer", "Communication" : "Languages spoken", "Native" : "Yoruba", "Studied with" : "English", "Learnt" : "Spanish", "id" : 2
}]
#get method using root ('/')
@app.get("/")
def testing():
    return {'reponse' : 'Salut World'}

#get method using root ('/comment')
@app.get("/posts")
def get_comments():
    return {'data' : my_posts}

#post method
@app.post("/posts")
def create_comments(post: Posts):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"mon reponse" : post_dict}

# getting specific post using id
@app.get('posts/{id}')
def get_specific_comment(id):
    print(id)