from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import json
app = FastAPI()

with open("urls.json", "r") as f:
    urls = json.load(f)

@app.get("/")
async def root():
    with open("index.html", "r") as file:
        return HTMLResponse(file.read())

@app.get("/{tag}/{slug}")
async def tag_slug(tag: str, slug: str):#
    return RedirectResponse(urls[tag][slug])

@app.get("/add/{slug}/{to}")
async def add(slug: str, to: str):
    urls["public"][slug] = to
    await _save()
    return Response()

@app.get("/add/{tag}/{slug}/{to}")
async def add(tag: str, slug: str, to: str):
    urls[tag][slug] = to
    await _save()
    return Response()

@app.post("/form/")
async def form(slug: str, link: str):
    await add(slug, link)
    with open("submitted.html", "r") as file:
        return HTMLResponse(file.read())
@app.get("/_save")
async def _save():
    with open("urls.json", "w") as file:
        json.dump(urls, file, indent=2, sort_keys=True)

@app.get("/{slug:path}")
async def slug_only(slug: str):
    if slug == "favicon.ico":
        return HTTPException(404)
    else:
        return RedirectResponse(f"https://{urls["public"][slug]}")