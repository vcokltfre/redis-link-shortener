from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

from src.auth import auth
from src.ls import Shortener

class Create(BaseModel):
    url: str
    name: Optional[str]

app = FastAPI(docs_url=None)
st = Shortener()

@app.get("/{linkid}")
async def get_page(linkid: str):
    return RedirectResponse(st.get(linkid), status_code=307)

@app.post("/create")
async def create_link(data: Create, request: Request):
    auth(request)

    return st.create(data.url, data.name)