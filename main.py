from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: Optional[bool] = False


class Database:
    def __init__(self):
        self.posts = []

    def get_posts(self):
        return self.posts

    def add_post(self, post: Post):
        post.id = str(uuid())
        self.posts.append(jsonable_encoder(post))
        return self.posts[-1]

    def get_post_by_id(self, post_id: str):
        for post in self.posts:
            if post["id"] == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found")

    def delete_post_by_id(self, post_id: str):
        for index, post in enumerate(self.posts):
            if post["id"] == post_id:
                self.posts.pop(index)
                return {"message": "Post has been deleted succesfully"}
        raise HTTPException(status_code=404, detail="Post not found")

    def update_post_by_id(self, post_id: str, updated_post: Post):
        for index, post in enumerate(self.posts):
            if post["id"] == post_id:
                self.posts[index] = jsonable_encoder(updated_post)
                return {"message": "Post has been updated succesfully"}
        raise HTTPException(status_code=404, detail="Post not found")

db = Database()

@app.get("/")
def read_root():
    return {"welcome": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return db.get_posts()

@app.post("/posts")
def save_post(post: Post):
    return db.add_post(post)

@app.get("/posts/{post_id}")
def get_post(post_id: str):
    return db.get_post_by_id(post_id)

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    return db.delete_post_by_id(post_id)

@app.put("/posts/{post_id}")
def update_post(post_id: str, updated_post: Post):
    return db.update_post_by_id(post_id, updated_post)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Server error"}
    )
