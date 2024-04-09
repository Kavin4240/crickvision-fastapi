from fastapi import FastAPI, HTTPException, Request,UploadFile,File,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from django.shortcuts import render, redirect
from django.contrib import auth
import pyrebase
from tempfile import SpooledTemporaryFile
from django.contrib.auth import logout
import requests
import numpy as np
from django.shortcuts import render
from django.contrib import auth
import os
from dotenv import load_dotenv
from models import currentUser, developer
load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
}
global curr_user

curr_user = None

firebase = pyrebase.initialize_app(config)
database = firebase.database()
authe = firebase.auth()
global local_id
global namex
global credit
global vcount

app = FastAPI()

templates_directory=r'F:\Intern\crickvision-fastapi\main\templates'
templates = Jinja2Templates(directory=templates_directory)

app.mount("/static/css", StaticFiles(directory=r"F:\Intern\crickvision-fastapi\main\static\css"), name="static/css")
app.mount("/static/js", StaticFiles(directory=r"F:\Intern\crickvision-fastapi\main\static\js"), name="static/js")
app.mount("/static/img", StaticFiles(directory=r"F:\Intern\crickvision-fastapi\main\static\img"), name="static/img")

# Home page
@app.get("/", response_class=HTMLResponse)
async def showWelcomePage(request:Request):
    print(request)
    return templates.TemplateResponse("index.html", {"request": request})
    
#Signin page
@app.get("/signin", response_class=HTMLResponse)
async def showSignin(request: Request):
   
    return templates.TemplateResponse("auth.html", {"request": request, "page":"signin"})

#Signup page
@app.get("/signup", response_class=HTMLResponse)
async def showSignup(request: Request):
    context = {"page": "signup"} 
    return templates.TemplateResponse("auth.html", {"request": request, **context})

#Forgotpassword
@app.get("/forgotpassword", response_class=HTMLResponse)
async def showForgotPass(request: Request): 
    return templates.TemplateResponse("auth.html", {"request": request})
 
    
#Forgotpass
@app.route("/forgotpass", methods=["GET", "POST"]) 
async def validateForgotPass(request: Request):
    form_data = await request.form()
    email = form_data.get("emailf")
    sendem = authe.send_password_reset_email(email)
    print(sendem)
    message = "A password reset email has been sent to " + sendem.get('email') + ", follow the steps there."
    return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})

@app.route("/signinvalidate", methods=["GET", "POST"])  
async def signInValidate(request:Request):
    global local_id
    global idtoken
    global credit
    global vcount
    global namex
    global curr_user
    form_data = await request.form()
    if request.method == "POST":
        email = form_data.get("emailx")
        password = form_data.get("passx")
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            if user is not None and "idToken" in user:
                idtoken = user["idToken"]
                user_info = authe.get_account_info(idtoken)
                email_verified = user_info['users'][0]['emailVerified']
                if email_verified:
                    fbdata = config
                    userid = user_info["users"][0]["localId"]
                    name = database.child("users").child(userid).child("details").child("name").get().val()
                    uType = database.child("users").child(userid).child("details").child("type").get().val()
                    if uType == "A":
                        curr_user = developer(name,userid)
                        testerx()
                        curr_user.getAllUsers()
                        names = curr_user.getNamelist()
                        emails = curr_user.getEmaillist()
                        user_ids = curr_user.getIdlist()
                        requests = curr_user.getRequestlist()
                        
                        uUrls = curr_user.getuUrlslist()
                        size = len(user_ids)
                        print(size)
                        zipped_lists = zip(names,emails,user_ids,requests,uUrls)
                        return templates.TemplateResponse("admin.html", {"request": request, "namex": name, "zipped_lists": zipped_lists})

                    else:
                        videocount = int(database.child("users").child(userid).child("details").child("videos").get().val())
                        curr_user = currentUser(name,userid,videocount)
                        block = curr_user.getBlock()
                        tester()
                        rprt = database.child("users").child(userid).child("details").child("report").get().val()
                        if rprt != None:
                            if rprt != "0":
                                rprtv = curr_user.fetchReportsV(database)
                                rprti = curr_user.fetchReportsI(database)
                                return templates.TemplateResponse("welcome.html", {"request": request, "name": name, "fbdata": fbdata, "userid": userid, "vcount": videocount, "rv": rprtv, "ri": rprti, "block": block, "report": "True"})


                        return templates.TemplateResponse("welcome.html", {"request": request, "name": name, "fbdata": fbdata, "userid": userid, "vcount": videocount, "block": block, "report": "True"})
                else:
                    message = "Email is not verified, kindly verify your Email before signing in!"
                    return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
            else:
                message = "User not found"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
        except Exception as e:
            
            msg = str(e)
            if "INVALID_LOGIN_CREDENTIALS" in msg:
                message = "Invalid Login Credentials, Forgot your password?"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in msg:
                message = "Too many Attempts, Try again later!"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
            else:
                message = "Internal Error!, Try Later"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
    return templates.TemplateResponse("auth.html", {"request": request, "page": "signin"})




@app.route("/signinvalidate", methods=["GET", "POST"])  
async def signInValidate(request:Request):
    global local_id
    global idtoken
    global credit
    global vcount
    global namex
    global curr_user
    form_data = await request.form()
    if request.method == "POST":
        email = form_data.get("emailx")
        password = form_data.get("passx")
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            if user is not None and "idToken" in user:
                idtoken = user["idToken"]
                user_info = authe.get_account_info(idtoken)
                email_verified = user_info['users'][0]['emailVerified']
                if email_verified:
                    fbdata = config
                    userid = user_info["users"][0]["localId"]
                    name = database.child("users").child(userid).child("details").child("name").get().val()
                    uType = database.child("users").child(userid).child("details").child("type").get().val()
                    if uType == "A":
                        curr_user = developer(name,userid)
                        testerx()
                        curr_user.getAllUsers()
                        names = curr_user.getNamelist()
                        emails = curr_user.getEmaillist()
                        user_ids = curr_user.getIdlist()
                        requests = curr_user.getRequestlist()
                        
                        uUrls = curr_user.getuUrlslist()
                        size = len(user_ids)
                        print(size)
                        zipped_lists = zip(names,emails,user_ids,requests,uUrls)
                        return templates.TemplateResponse("admin.html", {"request": request, "namex": name, "zipped_lists": zipped_lists})

                    else:
                        videocount = int(database.child("users").child(userid).child("details").child("videos").get().val())
                        curr_user = currentUser(name,userid,videocount)
                        block = curr_user.getBlock()
                        tester()
                        rprt = database.child("users").child(userid).child("details").child("report").get().val()
                        if rprt != None:
                            if rprt != "0":
                                rprtv = curr_user.fetchReportsV(database)
                                rprti = curr_user.fetchReportsI(database)
                                return templates.TemplateResponse("welcome.html", {"request": request, "name": name, "fbdata": fbdata, "userid": userid, "vcount": videocount, "rv": rprtv, "ri": rprti, "block": block, "report": "True"})


                        return templates.TemplateResponse("welcome.html", {"request": request, "name": name, "fbdata": fbdata, "userid": userid, "vcount": videocount, "block": block, "report": "True"})
                else:
                    message = "Email is not verified, kindly verify your Email before signing in!"
                    return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
            else:
                message = "User not found"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
        except Exception as e:
            
            msg = str(e)
            if "INVALID_LOGIN_CREDENTIALS" in msg:
                message = "Invalid Login Credentials, Forgot your password?"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in msg:
                message = "Too many Attempts, Try again later!"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
            else:
                message = "Internal Error!, Try Later"
                return templates.TemplateResponse("auth.html", {"request": request, "page": "signin", "msg": message})
    return templates.TemplateResponse("auth.html", {"request": request, "page": "signin"})

   
@app.get("/logout", response_class=HTMLResponse)   
async def logoutProcess(request:Request):
    apl = auth.logout(request)
    print(apl)
    return templates.TemplateResponse("auth.html", {"page": "signin", "msg": "Thank you, Visit again!"})

@app.route("/upload", methods=["GET", "POST"]) 
async def process_login(request: Request):
    if request.method == "POST":
        form_data = await request.form()
        name=form_data.get('name')
        email = form_data.get("emailx")
        password = form_data.get("passx") 
        print("Email:", email)
        print("Password:", password)
        
        # Perform login authentication logic here
        
        videocount = 1
        
        return templates.TemplateResponse("welcome.html", {"request": request, "videocount": videocount})
    else:
        # Handle GET request for /upload, maybe redirect or render an error page
        return {"message": "Method Not Allowed"}

@app.post("/uploadrequest")
async def uploadvideo(request: Request, video_file: UploadFile = File(...)):
    # Ensure that the uploaded file is an MP4 file
    if not video_file.filename.endswith(".mp4"):
        return "Only MP4 files are allowed"
    
    # Read the contents of the uploaded file
    contents = await video_file.read()
 
    
    # You can process or save the contents of the file here
    videocount = 1
    
    return templates.TemplateResponse("welcome.html", {"request": request,"videocount": videocount})

def tester():
    print("\nHiii")
    if (curr_user) is not None:
        print(curr_user.name)
        print(curr_user.userid)
        print(curr_user.credit)
        print(curr_user)
    else:
        print("Currently no user is logged in!\n")

def testerx():
    print("\nHiii Dev!")
    if (curr_user) is not None:
        print(curr_user.nme)
        print(curr_user.userid)
    else:
        print("Currently no user is logged in!\n")


@app.route("/process",methods=["GET","POST"])
async def videoProcess(request:Request):

    global vcount
    form_data = await request.form()
    vidUrl = form_data.get("vidUrl")
    local_id = form_data.get("us_id")
    fname = form_data.get("fname")
    uName = form_data.get("uName")
        
        
    curr_user.videoProcess(database,vidUrl,fname)
    curr_user.changeVcount(database)
    curr_user.submitRequest(database)
    curr_user.sendRequestMail(uName)
        
    bTr = curr_user.getBlock()
        
    return templates.TemplateResponse("welcome.html", {"request": request, "name": curr_user.name, "videocount": curr_user.videocount, "ss": "show", "block": bTr})

@app.post("/reportSubmit",response_class=HTMLResponse)
async def reportSubmit(request:Request):
    form_data = await request.form()
    vidUrl = form_data.get("vidUrl")
    
    vidURL = form_data.get("videou")
    userID = form_data.get("userid")
    images = form_data.POST.get("images")
    img_list = images.split(',')
    rName = form_data.get("rName")
    rMail = form_data.get("rMail")

    name = form_data.get("devname")
    print(vidURL,userID)
    database.child("users").child(userID).child("details").child("report").child("videos").set(vidURL)
    database.child("users").child(userID).child("details").child("report").child("images").set(img_list)
    database.child("users").child(userID).child("details").child("request").set("0")
    curr_user.send_email(rMail,rName)
    curr_user.getAllUsers()
    names = curr_user.getNamelist()
    emails = curr_user.getEmaillist()
    user_ids = curr_user.getIdlist()
    requests = curr_user.getRequestlist()
    uUrls = curr_user.getuUrlslist()
    size = len(user_ids)
    print(size)
    zipped_lists = zip(names,emails,user_ids,requests,uUrls)
    return templates.TemplateResponse("admin.html", {"request": request, "namex": name, "zipped_lists": zipped_lists, "notif": f"Mail Sent to {rMail}"})
 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3100, reload=True)       