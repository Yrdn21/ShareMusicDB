from fastapi import APIRouter, Request, HTTPException
from templating import templates

router = APIRouter(include_in_schema=False)

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request,"index.html")