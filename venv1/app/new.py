from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# my schema
class Post(BaseModel):
    Name: str
    Job: str
    rating: Optional[int] = None
    
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

# deleting specific post using id
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int):
    index = post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'comment with id : {id} is not on database')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

# updating comment
@app.put('/posts/{id}')
def update_comment(id: int, post: Post):
    index = post_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id : {id} is not on database")
    post_dict = post.dict()     #to put the post into a dictionary
    post_dict['id'] = id        #to indicate the id of the post in the dico
    my_posts[index] = post_dict     #to check and run code if the id matches the index in my_posts
    return{'data' : post_dict}