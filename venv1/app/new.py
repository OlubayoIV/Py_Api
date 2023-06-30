from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import schema

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
    
#get method using root ('/')
@app.get("/")
def root():
    return {'reponse' : 'Salut World'}

#get method using root ('/comment')
@app.get("/posts")
def get_comments():
    cursor.execute('''SELECT * FROM posts''') #passing a sql code to read the table initially created in pgadmin
    posts = cursor.fetchall() #fetching all data as i require all content of the table and passing it into a variable
    return {'data' : posts}


#post method 
@app.post("/posts", status_code=status.HTTP_201_CREATED) #including the right error code assigned with creating in CRUD, which is error 201
def create_comments(post: schema.Post): #creating a vague array of post to catch any post made by the user outside the one we provided
    cursor.execute('''INSERT INTO posts (name, job, published) VALUES (%s, %s, %s) RETURNING 
    * ''', #explained in my notes why %s was necessary ahead of the actual values
                   (post.name, post.job, post.published)) #these are case sensitive and must be in line with the schema even with the case values
    new_posts = cursor.fetchone() #since i'm sending a post fetchone is the applicable tool
    conn.commit() #this is like my save button when on pgadmin after creating new entry
    return {"mon reponse" : new_posts}

# getting specific post using id
@app.get('/posts/{id}')
def get_specific_comment(id : int): #passing int instructs any object passed to the ID as an integer
    cursor.execute('''SELECT * FROM posts WHERE id = %s''', (str(id))) #convert back to string to enable the %s effective
    post = cursor.fetchone()
    #post = find_post(id) #assigning the function earlier created that interated through posts for ID and passing it to the post
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with id : {id} was not found')
    return {"la detail" : post}

# deleting specific post using id
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT) #including the right error code assigned with deleting in CRUD, which is error 204
def delete_comment(id: int): #passing int instructs any object passed to the ID as an integer
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id)))
    supprim = cursor.fetchone()
    conn.commit()
    if not supprim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'comment with id : {id} is not on database')
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

# updating comment
@app.put('/posts/{id}')
def update_comment(id: int, post: schema.Post): #passing int instructs any object passed to the ID as an integer && creating a vague post to catch any input outside what we provided for the user
    cursor.execute('''UPDATE posts SET name = %s, job = %s, published = %s WHERE id = %s
      RETURNING *''', (post.name, post.job, post.published, (str(id))))
    
    change = cursor.fetchone()
    conn.commit()

    if change == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id : {id} is not on database")

    return{'data' : change}
