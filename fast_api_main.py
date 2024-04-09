# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from models import User, Video
# from main.views import (
#     signin_user,
#     logout_user,
#     process_video,
#     upload_video
# )

# app = FastAPI()



# @app.post("/logout")
# async def logout():
#     # Implement logout functionality
#     logout_user()
#     return {"message": "Logged out successfully"}

# @app.post("/process_video")
# async def process_video_endpoint(video_id: int):
#     # Implement video processing functionality
#     processed_video = process_video(video_id)
#     if processed_video:
#         return {"message": "Video processed successfully"}
#     else:
#         return JSONResponse(status_code=404, content={"message": "Video not found"})

# @app.post("/upload_video")
# async def upload_video_endpoint(video_data: bytes):
#     # Implement video upload functionality
#     video_id = upload_video(video_data)
#     return {"message": f"Video uploaded successfully with ID: {video_id}"}






















# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from django.shortcuts import render, redirect
# from django.contrib import auth
# import pyrebase
# from django.contrib.auth import logout
# import requests
# import numpy as np
# from django.shortcuts import render
# from django.contrib import auth
# import os
# from dotenv import load_dotenv
# from models import currentUser, developer
# load_dotenv()


# config = {
#     "apiKey": os.getenv("FIREBASE_API_KEY"),
#     "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
#     "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
#     "projectId": os.getenv("FIREBASE_PROJECT_ID"),
#     "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
#     "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
#     "appId": os.getenv("FIREBASE_APP_ID"),
#     "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
# }
# global curr_user

# curr_user = None



# firebase = pyrebase.initialize_app(config)
# database = firebase.database()
# authe = firebase.auth()
# global local_id
# global namex
# global credit
# global vcount

# app = FastAPI()
# templates_directory=r'F:\Intern\crickvision-fastapi\main\templates'
# templates = Jinja2Templates(directory=templates_directory)

# app.mount("/static/css", StaticFiles(directory=r"F:\Intern\crickvision-fastapi\main\static\css"), name="static/css")
# app.mount("/static/js", StaticFiles(directory=r"F:\Intern\crickvision-fastapi\main\static\js"), name="static/js")
# app.mount("/static/img", StaticFiles(directory=r"F:\Intern\crickvision-fastapi\main\static\img"), name="static/img")

# def showWelcomePage(request):
#     print(request)
#     return render(request, "index.html")

# # def showSignin(request):
# #     return render(request, "auth.html",{"page":"signin"})

# @app.get("/signin", response_class=HTMLResponse)
# async def showSignin(request: Request):
#     return templates.TemplateResponse("auth.html", {"request": request, "page": "signin"})

# def showSignup(request):
#     return render(request, "auth.html",{"page":"signup"})

# def showForgotPass(request):
#     return render(request, "auth.html",{"page":"forgotpass"})

# def validateForgotPass(request):
#     if request.method == "POST":
#         email = request.POST.get('emailf')
#         sendem = authe.send_password_reset_email(email)
#         print(sendem)
#         message = "An password reset email has been sent to " + sendem.get('email') +", follow the steps there."
#         return render(request,"auth.html",{"page":"signin","msg":message})
    
# def signInValidate(request):
#     global local_id
#     global idtoken
#     global credit
#     global vcount
#     global namex
#     global curr_user
#     if request.method == "POST":
#         email = request.POST.get("emailx")
#         password = request.POST.get("passx")
#         try:
#             user = authe.sign_in_with_email_and_password(email, password)
#             if user is not None and "idToken" in user:
#                 idtoken = user["idToken"]
#                 user_info = authe.get_account_info(idtoken)
#                 email_verified = user_info['users'][0]['emailVerified']
#                 if email_verified:
#                     fbdata = config
#                     userid = user_info["users"][0]["localId"]
#                     name = database.child("users").child(userid).child("details").child("name").get().val()
#                     uType = database.child("users").child(userid).child("details").child("type").get().val()
#                     if uType == "A":
#                         curr_user = developer(name,userid)
#                         testerx()
#                         curr_user.getAllUsers()
#                         names = curr_user.getNamelist()
#                         emails = curr_user.getEmaillist()
#                         user_ids = curr_user.getIdlist()
#                         requests = curr_user.getRequestlist()
                        
#                         uUrls = curr_user.getuUrlslist()
#                         size = len(user_ids)
#                         print(size)
#                         zipped_lists = zip(names,emails,user_ids,requests,uUrls)
#                         return render(request,"admin.html", {"namex":name,"zipped_lists":zipped_lists})

#                     else:
#                         videocount = int(database.child("users").child(userid).child("details").child("videos").get().val())
#                         curr_user = currentUser(name,userid,videocount)
#                         block = curr_user.getBlock()
#                         tester()
#                         rprt = database.child("users").child(userid).child("details").child("report").get().val()
#                         if rprt != None:
#                             if rprt != "0":
#                                 rprtv = curr_user.fetchReportsV(database)
#                                 rprti = curr_user.fetchReportsI(database)
#                                 return render(request,"welcome.html", {"name":name, "fbdata": fbdata, "userid": userid,"vcount":videocount,"rv":rprtv,"ri":rprti,"block": block,"report":"True"})


#                         return render(request,"welcome.html", {"name":name, "fbdata": fbdata, "userid": userid,"vcount":videocount, "block": block,"report":"True"})
#                 else:
#                     message = "Email is not verified, kindly verify your Email before signing in!"
#                     return render(request, "auth.html",{"page":"signin","msg":message})
#             else:
#                 message = "User not found"
#                 return render(request, "auth.html", {"page":"signin","msg": message})
#         except Exception as e:
            
#             msg = str(e)
#             if "INVALID_LOGIN_CREDENTIALS" in msg:
#                 message = "Invalid Login Credentials, Forgot your password?"
#                 return render(request, "auth.html", {"page":"signin","msg": message})
#             elif "TOO_MANY_ATTEMPTS_TRY_LATER" in msg:
#                 message = "Too many Attempts, Try again later!"
#                 return render(request, "auth.html", {"page":"signin","msg": message})
#             else:
#                 message = "Internal Error!, Try Later"
#                 return render(request, "auth.html", {"page":"signin","msg": message})
#     return render(request, "auth.html",{"page":"signin"})
    
# def signUpValidate(request):
#     global local_id
#     name = request.POST.get("name")
#     email = request.POST.get("email")
#     passw = request.POST.get("pass")
#     try:
#         user = authe.create_user_with_email_and_password(email, passw)
#         authe.send_email_verification(user["idToken"])
#         uid = user["localId"]
#         local_id = uid
#         data = {
#         "name": name,
#         "status": "1",
#         "email": email,
#         "videos": 0,
#         "credit": 1,
#         "type": "U",
#         "request": "0",
#         }
#         msg = "An verification Email has been sent to your email, Verify your email and proceed to login"
#         database.child("users").child(uid).child("details").set(data)
#         return render(request, "auth.html",{"msg":msg,"page":"signin"})
#     except Exception as e:
#         msg = "Unable to create account. Try again"
#         return render(request, "auth.html", {"msg":msg,"page":"signin"})
    
# def logoutProcess(request):
#     apl = auth.logout(request)
#     print(apl)
#     return render(request,"auth.html",{"page":"signin","msg":"Thank you, Visit again!"})

# def uploadVideo(request):
#     global idtoken
#     if request.method == "POST":
#         something = request.POST.get("videoFile")
#         print(something)
#     return render(request,"welcome.html")

# def tester():
#     print("\nHiii")
#     if (curr_user) is not None:
#         print(curr_user.name)
#         print(curr_user.userid)
#         print(curr_user.credit)
#         print(curr_user)
#     else:
#         print("Currently no user is logged in!\n")

# def testerx():
#     print("\nHiii Dev!")
#     if (curr_user) is not None:
#         print(curr_user.nme)
#         print(curr_user.userid)
#     else:
#         print("Currently no user is logged in!\n")



# def videoProcess(request):

#     global vcount
#     if request.method == "POST":
#         vidUrl = request.POST.get("vidUrl")
#         local_id = request.POST.get("us_id")
#         fname = request.POST.get("fname")
#         uName = request.POST.get("uName")
#         curr_user.videoProcess(database,vidUrl,fname)
#         curr_user.changeVcount(database)
#         curr_user.submitRequest(database)
#         curr_user.sendRequestMail(uName)
        
#         bTr = curr_user.getBlock()

        
#         return render(request,"welcome.html", {"name":curr_user.name,"videocount":curr_user.videocount, "ss": "show","block":bTr})

# def reportSubmit(request):
#     if request.method == "POST":
#         vidURL = request.POST.get("videou")
#         userID = request.POST.get("userid")
#         images = request.POST.get("images")
#         img_list = images.split(',')
#         rName = request.POST.get("rName")
#         rMail = request.POST.get("rMail")

#         name = request.POST.get("devname")
#         print(vidURL,userID)
#         database.child("users").child(userID).child("details").child("report").child("videos").set(vidURL)
#         database.child("users").child(userID).child("details").child("report").child("images").set(img_list)
#         database.child("users").child(userID).child("details").child("request").set("0")
#         curr_user.send_email(rMail,rName)
#         curr_user.getAllUsers()
#         names = curr_user.getNamelist()
#         emails = curr_user.getEmaillist()
#         user_ids = curr_user.getIdlist()
#         requests = curr_user.getRequestlist()
#         uUrls = curr_user.getuUrlslist()
#         size = len(user_ids)
#         print(size)
#         zipped_lists = zip(names,emails,user_ids,requests,uUrls)
#         return render(request,"admin.html", {"namex":name,"zipped_lists":zipped_lists, "notif": f"Mail Sent to {rMail}"})
 
 
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)       