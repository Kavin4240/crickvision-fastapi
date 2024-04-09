class currentUser:
    userid = ''
    videocount = 0
    name = ''
    credit = 1
    sMail = 'kavinkumar2628@gmail.com'
    sPass = 'zjwa aihu lzzi hbfz'
    devMail = "2k21aids66@kiot.ac.in"
    def __init__(self,n,idx,vc):
        self.userid = idx
        self.videocount = vc
        self.name = n

    def getCredit(self):
        if (self.videocount > 1):
            self.credit = 0
        else:
            self.credit = 1
        return self.credit

    def changeVcount(self,db):
        self.videocount += 1
        db.child("users").child(self.userid).child("details").child("videos").set(self.videocount)
        return True
    
    def getBlock(self):
        if (self.videocount >= self.credit ):
            block = True
        else:
            block = False
        return block
    
    def videoProcess(self,db,url,fname):
        db.child("users").child(self.userid).child("details").child("uploads").child(fname).child().set(url)
    
    def submitRequest(self,db):
        db.child("users").child(self.userid).child("details").child("request").set("1")

    def fetchReportsV(self,db):
        vids = db.child("users").child(self.userid).child("details").child("report").child("videos").get().val()
        return vids
    def fetchReportsI(self,db):
        imgs = db.child("users").child(self.userid).child("details").child("report").child("images").get().val()
        print(imgs)
        return imgs
    
    def sendRequestMail(self,name):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
    
        message = MIMEMultipart()
        message['From'] = self.sMail
        message['To'] = self.devMail
        message['Subject'] = "New Video Process Request!"
        body = f"{name} submitteed a new Request!, Hop into portal and accomplish the work ASAP!"
        message.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sMail, self.sPass)
            server.sendmail(self.sMail, self.devMail, message.as_string())

class developer:
    userid = ""
    nme = ""
    names = []
    emails = []
    ids = []
    request = []
    uUrls = []
    sMail = 'kavinkumar2628@gmail.com'
    sPass = 'zjwa aihu lzzi hbfz'
    import os
    from dotenv import load_dotenv
    import pyrebase

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
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

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    def __init__(self,n,idx):
        self.userid = idx
        self.nme = n
        self.names = []
        self.emails = []
        self.ids = []
        self.request = []
        self.uUrls = []



    def getAllUsers(self):
        def addDetails(self,uId):
            uType = self.db.child("users").child(uId).child("details").child("type").get().val()
            if uType != "A":
                uReq = self.db.child("users").child(uId).child("details").child("request").get().val()
                if uReq != "0":
                    uName = self.db.child("users").child(uId).child("details").child("name").get().val()
                    self.names.append(uName)
                    uMail = self.db.child("users").child(uId).child("details").child("email").get().val()
                    self.emails.append(uMail)
                    self.ids.append(uId)
                    self.request.append(uReq)
                    uUrl = self.db.child("users").child(uId).child("details").child("uploads").child("video1").get().val()
                    self.uUrls.append(uUrl)



        all_users = self.db.child("users").get()
        print(all_users)
        all_user_ids = self.db.child("users").shallow().get()
        adara = all_user_ids.val()
        adara = list(adara)
        self.names = []
        self.emails = []
        self.request = []
        self.uUrls = []
        self.ids = []
        for i in range(0,len(adara)):
            print(adara[i])
            addDetails(self,adara[i])

        print(self.names)
        print(self.emails)
        print(self.ids)

    def getNamelist(self):
        return self.names
    def getIdlist(self):
        return self.ids
    def getEmaillist(self):
        return self.emails
    def getRequestlist(self):
        return self.request
    def getuUrlslist(self):
        return self.uUrls

    def send_email(self,mail,name):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
    
        message = MIMEMultipart()
        message['From'] = self.sMail
        message['To'] = mail
        message['Subject'] = "Your Video has been Analysed by our AI!"
        body = f"Dear {name}!, \n\nYour Uploaded video has been analysed by our Developers and available in REPORTS section of your profile. \n\nBy,\nThe Crickvision Team❤"
        message.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sMail, self.sPass)
            server.sendmail(self.sMail, mail, message.as_string())