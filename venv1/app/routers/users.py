from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import schemas, utils
import psycopg2
from psycopg2.extras import RealDictCursor

# creating a connection with my pg admmin
try:
    conn = psycopg2.connect(host='localhost', database='api_py', user='postgres', password='united1234',
    cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print('Database connection was succesful!')
except Exception as error:
    print('Connection to database failed')
    print('Error: ', error)

router = APIRouter()
#post for users
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UsersOut)
def create_comments(user: schemas.Users):
    
    #completing the hash password sequence
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    cursor.execute('''INSERT INTO users (email, password) VALUES (%s, %s) RETURNING 
    * ''', (user.email, user.password))
    new_users = cursor.fetchone() 
    conn.commit() 
    return new_users


@router.get('/users/{id}', response_model=schemas.UsersOut)
def get_specific_user(id : int):
    cursor.execute('''SELECT * FROM users WHERE id = %s''', (str(id),))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'user with id : {id} was not found')
    return user