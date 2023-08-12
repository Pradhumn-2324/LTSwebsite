from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from config.db import conn,db,users_collection
from models.admin_login import Employee
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Form
from models.tokenmng import verify_password,create_access_token,get_password_hash

app = FastAPI()
flag = False

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
form_data : OAuth2PasswordRequestForm = Depends()




@app.get("/")
async def root(request: Request):

    # Render the template
    return templates.TemplateResponse("index.html", {"request": request})




@app.get("/admin")
async def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.post("/admin")
async def login_admin(username: str = Form(...), password: str = Form(...)):
    user = await users_collection.find_one({"username": username})
    print(get_password_hash(password))
    if user and verify_password(password, user["password"]):
        flag = True
        redirect_url = f"/admin/{username}/home"
        return HTMLResponse(content=f'<meta http-equiv="refresh" content="0;url={redirect_url}">', status_code=307)
        # raise HTTPException(status_code=307, detail="Redirecting...", headers={"Location": redirect_url})
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@app.get("/admin/{admin_name}/home")
async def admin_home(request: Request, admin_name: str = None):
    user = await users_collection.find_one({"username": admin_name})
    if user and user["username"]==admin_name:
        return templates.TemplateResponse("AdminHome.html", {"request": request, "admin_name": admin_name,"flag":flag})
    raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/admin/{admin_name}/registeremp")
async def admin_register(request:Request ,admin_name: str = None):
    user = await users_collection.find_one({"username": admin_name})
    if user and user["username"] == admin_name:
        return templates.TemplateResponse("emp_register.html",
                                          {"request": request, "admin_name": admin_name, "flag": flag})
    raise HTTPException(status_code=401, detail="Not authenticated")


@app.post("/myemployee")
async def add_employee(employee : Employee):
    employee_data =  employee.dict()
    print("hello employee")
    print(employee_data)



@app.get("/admin/{admin_name}/employees")
async def admin_register(request:Request ,admin_name: str = None):
    user = await users_collection.find_one({"username": admin_name})
    if user and user["username"] == admin_name:
        return templates.TemplateResponse("myemployee.html",
                                          {"request": request, "admin_name": admin_name, "flag": flag})
    raise HTTPException(status_code=401, detail="Not authenticated")

