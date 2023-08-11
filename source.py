from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.db import conn,db,users_collection
from models.admin_login import admin_log
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Form


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




@app.get("/")
def root(request: Request):
    template_data = {"page_title": "FastAPI Template Example"}

    # Render the template
    return templates.TemplateResponse("index.html", {"request": request, "data": template_data})


@app.get("/admin")
def root(request: Request):
    template_data = {"page_title": "FastAPI Template Example"}
    return templates.TemplateResponse("admin_login.html", {"request": request, "data": template_data})

form_data : OAuth2PasswordRequestForm = Depends()


@app.post("/ad_login")
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.password)
    user = users_collection.find_one({"username":form_data.username,"password":form_data.password})

    print(form_data.username)
    if user:
        print("yes success")
        try:
            response= RedirectResponse(url=f"/Admin_Home/{form_data.username}")
            response.status_code=302
            return response
        except:
            print("error")
        # return templates.TemplateResponse("adminlog.html",{"request": })
    else:
        raise HTTPException(status_code=405 ,detail="Credentials not matched")


@app.get("/Admin_Home/{admin_name}")
async def admin_home(request: Request, admin_name: str, token: str = Depends(oauth2_scheme)):
    print(f"Received token: {token}")
    if users_collection.find_one({"username": token}):
        print("Authenticated!")
        return templates.TemplateResponse("AdminHome.html", {"request": request, "admin_name": admin_name})
    else:
        print("Not authenticated!")
        raise HTTPException(status_code=401, detail="Not authenticated")

