from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# my schema
class Post(BaseModel):
    Name: str
    Job: str
    #rating: Optional[int] = None
    Published: bool = True

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
    
#get method using root ('/')
@app.get("/")
def root():
    return {'reponse' : 'Salut World'}

#get method using root ('/comment')
@app.get("/posts")
def get_comments():
    cursor.execute('''SELECT * FROM posts''')
    posts = cursor.fetchall()
    return {'data' : posts}

#post method 
@app.post("/posts", status_code=status.HTTP_201_CREATED) #including the right error code assigned with creating in CRUD, which is error 201
def create_comments(post: Post): #creating a vague array of post to catch any post made by the user outside the one we provided
    post_dict = post.dict() #make that post a doctionary and assign it to this function
    post_dict['id'] = randrange(0, 1000000) #using randrange to generate a random number between 0 - 1000000 for the id
    my_posts.append(post_dict) #appending it with the original post
    return {"mon reponse" : post_dict}

# getting specific post using id
@app.get('/posts/{id}')
def get_specific_comment(id : int): #passing int instructs any object passed to the ID as an integer
    post = find_post(id) #assigning the function earlier created that interated through posts for ID and passing it to the post
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id : {id} was not found')
    return {"la detail" : post}

# deleting specific post using id
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT) #including the right error code assigned with deleting in CRUD, which is error 204
def delete_comment(id: int): #passing int instructs any object passed to the ID as an integer
    index = post_index(id) #assigning the function earlier created that enumerated ID value in post and passing it to the post_index
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'comment with id : {id} is not on database')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

# updating comment
@app.put('/posts/{id}')
def update_comment(id: int, post: Post): #passing int instructs any object passed to the ID as an integer && creating a vague post to catch any input outside what we provided for the user
    index = post_index(id) #assigning the function earlier created that enumerated ID value in post and passing it to the post_index
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id : {id} is not on database")
    post_dict = post.dict()     #to put the post into a dictionary
    post_dict['id'] = id        #to indicate the id of the post in the dico
    my_posts[index] = post_dict     #to check and run code if the id matches the index in my_posts
    return{'data' : post_dict}