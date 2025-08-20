from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/fornecedor/dashboard")
async def get_root():
    response = templates.TemplateResponse("/dashboard.html", {"request": {}})
    return response

