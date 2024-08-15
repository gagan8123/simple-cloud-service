from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse    
import sqlite3
from backend_app.file_cmd import *
from  backend_app.pyform import UploadFileForm
from django.core.files.storage import FileSystemStorage
# from django.core.files.storage import FileSystemStorage
from django.conf import settings
import math
import smtplib
from email.message import EmailMessage

# Create your views here.
v = oscmd('cd')
path = v[:len(v)-1]+"\\static\\"
max_storage = math.pow(1024,3)
gb = 2 #gb

def check_session(req):
    
    val = req.session.get("login",False)
    if val:
        total_stored = int(data_stored(path+str(req.session['folder'])))
        print(gb)
        total_strored_bytes_to_gb = round(total_stored/max_storage,5)
        percentage = (total_strored_bytes_to_gb/gb)*100
        print("percent",percentage)
        print("total_storedt",total_strored_bytes_to_gb)
        return render(req,"home.html",{"storage":total_strored_bytes_to_gb,"percentage":int(percentage)})
    return render(req,"login_page.html")




def signup(requests):
    val = requests.session.get("login",False)
    if val:
        return HttpResponseRedirect("/")
    return render(requests,"signup.html")
def createUser(requests):

    if requests.method == "POST":
        try:
            uname = requests.POST.get('uname')
            passs = requests.POST.get('pass')
            conn = sqlite3.connect("django_database.db")
            cursor = conn.cursor()
            res = cursor.execute("insert into user_login1(user_email,user_pass) values(?,?)",(uname,passs))
            print(res)
            conn.commit()


            res = cursor.execute("select user_id from user_login1").fetchall()
            print(res)
            create_folder(path+str(res[-1][0]))
            create_folder(path+str(res[-1][0])+"\\documents")
            create_folder(path+str(res[-1][0])+"\\images")
            create_folder(path+str(res[-1][0])+"\\videos")
            conn.close()
            return render(requests,"login_page.html")
        except Exception as e: 
            print(e)
            conn.close()
            return render(requests,"signup.html")
            
    else:
        render(requests,"signup.html")

def access(requests):
    val = requests.session.get("login","")
    if val:
        return HttpResponseRedirect("/")
    elif requests.method == "POST":
        try:
            uname = requests.POST.get('uname')
            passs = requests.POST.get('pass')
            conn = sqlite3.connect("django_database.db")
            cursor = conn.cursor()
            res = cursor.execute("select * from user_login1 where user_email = ?  and user_pass = ?;",(uname,passs)).fetchall()
            conn.close()
            if len(res) == 1:
                print(res[0][0])
                requests.session['login'] = True
                requests.session['folder'] = res[0][0]
                return HttpResponseRedirect("/")
            cursor = conn.cursor()
        except :
            conn.close()
        return render(requests,"login_page.html")
    else:
        return render(requests,"login_page.html")
    
def files(request):
    val = request.session.get("login",False)
    if val:
        return render(request,"file_display.html")
    return render(request,"login_page.html")

def logout(request):
    del request.session['login']
    del request.session['folder']
    return HttpResponseRedirect("/login")



def document_display(request):
    user_path = path+str(request.session['folder'])+"\\"+request.GET.get("path","")
    user_path = user_path.replace(".","")
    user_path = user_path.replace("//","/")
    user_path = user_path.replace("&","")
    print(user_path)
    #print(oscmd(f'for %i in ({user_path}\\*) do @if not exist %i\@echo %~nxi')).pop()
    folders = (oscmd(f"for /d %i in (\"{user_path}\\*\") do @echo %~nxi").split("\n"))
    files = oscmd(f'for %f in (\"{user_path}\\*.*\") do @echo %~nxf').split("\n")
    folders.pop()
    files.pop()
    path1 = user_path[user_path.index("\static"):]
    path1 = path1.replace("\\","/")
    print(path1)
    print(user_path)
    # file_path = "\\static\\"+str(request.session['folder'])+"\\"+request.POST.get("path","")
    # print(file_path)
    dic = {"folder":folders,"files":files,"path":path1,"origin":request.GET.get("path","")}
    
    return render(request,"myfile.html",dic)



def create_folder1(req):
    if req.method == "POST":
        user_path = path+str(req.session['folder'])
        origin = req.POST.get("origin","")
        folder_name = req.POST.get("folder_name","")
        if origin and folder_name:
            o = origin.replace("/","\\")
            create_folder(user_path+"\\"+o+"\\"+folder_name)
    return HttpResponseRedirect("/cloud/drivefiles?path="+origin)

def upload_file(request):
    print("upload file")
    origin = request.POST.get("origin","")
    if request.method == 'POST' and request.FILES.get('file',0):
        print(request.FILES.get("file"))
        file = request.FILES.get('file',0)
        print(file)
        if(file):
            user_path = path+str(request.session.get("folder"))+"\\"+origin
            fs = FileSystemStorage(location=user_path)
            fs.save(file.name,file)
            if(check_file_stirage(path+str(request.session.get("folder")))):
                delete_file(user_path+"\\"+file.name)


            
            #return HttpResponseRedirect("/cloud/drivefiles?path="+origin)
        print("origin",origin)
        return HttpResponseRedirect("/cloud/drivefiles?path="+origin)  
    


def del_file(request):
    p = path
    print()
    print()
    if request.method == "POST":
        print("hello")
        print()
        print()
        a = list(str(request.POST.get("path[]")).split(","))
        origin = request.POST.get("origin")
        print(a)
        for i in a:
            i = i.replace("/static/","",1)
            i = i.replace("/","\\")
            
            print(path+i)
            delete_file(path+i)
        


    return HttpResponseRedirect("/cloud/drivefiles?path="+origin) 



def del_folder(requests):
    if requests.method == "POST":
        origin = requests.POST.get("origin")
        folder = requests.POST.get("folder")
        folder = folder.replace("/","\\")
        print(path+str(requests.session.get("folder"))+"\\"+folder)
        delete_folder(path+str(requests.session.get("folder"))+"\\"+folder)
        return HttpResponseRedirect("/cloud/drivefiles?path="+origin)
    

def send_email(email,password):
    try:
        your_email_id = ""
        your_app_pass = ""
        to_email = email
        msg =EmailMessage()
        message = f"""
dear user 

    you have requested for your forgotten password and your password of the cloud storage is {password}

thank you
cloud storage
safe storage
"""
        msg.set_content(message)
        msg['From'] = your_email_id
        msg['To'] = email
        msg["Subject"] = "cloud storage password"
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(your_email_id,your_app_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False
    
def forgotpass(req):
    email = req.GET.get("email",None)
    print(email)
    flag = 0
    if email:
        conn = sqlite3.connect("django_database.db")
        cursor = conn.cursor()
        user_pass = cursor.execute(f"select user_pass from user_login1 where user_email = '{email}';").fetchall()
        print(user_pass)
        if user_pass:
            send_email(email,user_pass[0][0])
            return JsonResponse({"res":"successfully sent"})
        
    return JsonResponse({"res":"eamil not found"})
    


            