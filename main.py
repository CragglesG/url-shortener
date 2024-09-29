from typing import Annotated

from fastapi import FastAPI, Response, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
import json

app = FastAPI()

with open("urls.json", "r") as f:
    urls = json.load(f)

@app.get("/")
async def root():
    with open("index.html", "r") as file:
        return HTMLResponse(file.read())


@app.get("/add/{slug}/{to}")
async def add(slug: str, to: str):
    urls["public"][slug] = to
    await _save()
    return Response()

@app.post("/form")
async def form(slug: Annotated[str, Form()], link: Annotated[str, Form()]):
    await add(slug=slug, to=link)
    with open("submitted.html", "r") as file:
        return HTMLResponse(file.read())
@app.get("/_save")
async def _save():
    with open("urls.json", "w") as file:
        json.dump(urls, file, indent=2, sort_keys=True)

@app.get("/{slug}")
async def slug_only(slug: str):
    if slug == "favicon.ico":
        return HTTPException(404)
    else:
        return RedirectResponse(urls["public"][slug])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)