from pydantic import BaseModel, EmailStr
from datetime import datetime
# my schema for posts
class Post(BaseModel):
    name: str
    job: str
    #rating: Optional[int] = None
    published: bool = True

    # my schema for users
class Users(BaseModel):
    email: EmailStr
    password: str

    
# my schema for users response
class UsersOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime