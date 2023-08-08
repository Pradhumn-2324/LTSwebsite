from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.db import conn,db,users_collection
from models.admin_login import admin_log
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def check_logged_in_user(token: str = Depends(oauth2_scheme)):
    if users_collection.find_one({"username": token}):
        return True
    else:
        return False

@app.get("/")
def root(request: Request):
    template_data = {"page_title": "FastAPI Template Example"}

    # Render the template
    return templates.TemplateResponse("index.html", {"request": request, "data": template_data})

@app.get("/admin")
def root(request: Request):
    template_data = {"page_title": "FastAPI Template Example"}
    return templates.TemplateResponse("admin_login.html", {"request": request, "data": template_data})


@app.post("/ad_login")
async def login_admin(form_data : OAuth2PasswordRequestForm = Depends()):

    user = users_collection.find_one({"username":form_data.username,"password":form_data.password})
    print(user)
    if user:
        print("yes success")
        try:
            return RedirectResponse(url=f"/Admin_Home/{form_data.username}")
        except:
            print("error")
        # return templates.TemplateResponse("adminlog.html",{"request": })
    else:
        raise HTTPException(status_code=405 ,detail="Credentials not matched")


@app.get("/Admin_Home/{admin_name}")
async def admin_home(request: Request, admin_name: str, logged_in: bool = Depends(check_logged_in_user)):
    print(1)
    if logged_in:
        return templates.TemplateResponse("AdminHome.html", {"request": request, "admin_name": admin_name})
    else:
        raise HTTPException(status_code=401, detail="Not logged in")
