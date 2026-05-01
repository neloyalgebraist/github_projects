from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author": "Neloy Ghosh",
        "title": "FastAPI is awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "May 1, 2026",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is great for web development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "May 2,2026",
    },
]


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get("/api/posts")
def get_posts():
    return posts
