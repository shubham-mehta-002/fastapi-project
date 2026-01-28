from fastapi import FastAPI, HTTPException 
from data.posts import posts
from app.schemas import PostCreate, PostResponse

app = FastAPI()

@app.get("/posts")
def get(limit : int = None) -> list[PostResponse]:
    if limit:
        return posts[:limit]
    return posts


@app.get("/posts/{id}")
def get_post_by_id(id: int) -> PostResponse:
    for post in posts:
        if post["id"] == id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")  


@app.post("/posts")
def create_post(post : PostCreate) -> PostResponse:
    new_post = post.dict()
    new_post["id"] = posts[-1]["id"] + 1 if posts else 1
    posts.append(new_post)
    return posts[-1]


@app.delete("/posts/{id}")
def delete_post(id : int) -> PostResponse:
    for index, post in enumerate(posts):
        if post["id"] == id:
            deleted_post = posts.pop(index)
            return deleted_post
        
    raise HTTPException(status_code=404, detail="Post not found")