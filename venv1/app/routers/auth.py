from fastapi import APIRouter, HTTPException, Response, status, Request
from .. import utils, schemas
import psycopg2
from psycopg2.extras import RealDictCursor
#import requests

# creating a connection with my pg admmin
try:
    conn = psycopg2.connect(host='localhost', database='api_py', user='postgres', password='united1234',
    cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was succesful!')
except Exception as error:
    print('Connection to database failed')
    print('Error: ', error)

#creating router to house prefix and tags to make code cleaner
router = APIRouter(
    tags=['Authentication']
)

#users login verification and password hashing
@router.post('/login')
def login(login: schemas.UsersLogin):

    cursor.execute('''SELECT * FROM users WHERE email = %s''', (str(login.email),)) #convert back to string to enable the %s effective
    user = cursor.fetchone()
    #post = find_post(id) #assigning the function earlier created that interated through posts for ID and passing it to the post
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'Invalid credential')
    #return login

    if not utils.verify(login.password, user["password"]): #the password was an array that was why i kept getting an internal server error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    
    return {'token'}