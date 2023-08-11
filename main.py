from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from config.db import conn,db,users_collection
from models.admin_login import admin_log
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Form
from models.tokenmng import verify_password,create_access_token,get_password_hash

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
form_data : OAuth2PasswordRequestForm = Depends()




@app.get("/")
async def root(request: Request):

    # Render the template
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if user and verify_password(form_data.password, user["password"]):
        access_token = create_access_token({"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@app.get("/admin")
async def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.post("/admin")
async def login_admin(username: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"username": username})
    print(get_password_hash(password))
    if user and verify_password(password, user["password"]):
        # response = RedirectResponse(url=f"/Admin_Home/{username}")
        # response.status_code=307
        # response = RedirectResponse(url=f"/admin/{username}")
        # return response
        redirect_url = f"/admin/{username}"
        return HTMLResponse(content=f'<meta http-equiv="refresh" content="0;url={redirect_url}">', status_code=307)
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@app.get("/admin/{admin_name}")
async def admin_home(request: Request, admin_name: str = None):
    user = await users_collection.find_one({"username": admin_name})
    if user and user["username"]==admin_name:
        return templates.TemplateResponse("AdminHome.html", {"request": request, "admin_name": admin_name})
    raise HTTPException(status_code=401, detail="Not authenticated")


