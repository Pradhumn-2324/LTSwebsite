from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root(request: Request):
    template_data = {"page_title": "FastAPI Template Example"}

    # Render the template
    return templates.TemplateResponse("index.html", {"request": request, "data": template_data})
