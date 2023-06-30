from pydantic import BaseModel

# my schema
class Post(BaseModel):
    name: str
    job: str
    #rating: Optional[int] = None
    published: bool = True