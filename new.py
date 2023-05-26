from fastapi import FastAPI

app = FastAPI()

# get method using root ('/')
@app.get("/")
async def testing():
    return {'reponse' : 'Salut World'}

#get method using root ('/posts')
@app.get("/comments")
def get_comments():
    return {'data' : 'votre reponse est ici'}