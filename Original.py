#!/usr/bin/env python
# coding: utf-8

# In[17]:


import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import time
from threading import Thread

now = datetime.now()

app = Flask(__name__, static_url_path ="/static")

UPLOAD_FOLDER = r'/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt','csv'}
secret_key = "kapil"

if "members.txt" in os.listdir():
    pass
else:
    my_file = open("members.txt","+a")
    my_file.write("login;password;name\n")
    my_file.close()



DIR_PATH =r'/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

email ="_"
password="_"
name = "_"
c=0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_file():
    return render_template('__init__.html')


@app.route('/get-text', methods=['GET', 'POST'])
def foo():
    global bar, email
    email = request.form.get('Email')
    password = request.form.get('Password')
    register = request.form.get('register')
    if register == "y" or register == "Y" :
        return render_template('new_acc.html')
    my_file = open("members.txt","r")
    if (email == None or email == "email " or password == None or password ==  " pass"):
        return render_template('__init__.html')
    my_file = open("members.txt","r")
    for i in my_file:
        if email in i.split(";")[0]:
            if password in i.split(";")[1]:
                bar = i.split(";")[2]
                UPfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/upload".format(bar[:-1],email))
                DWfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email))
                return render_template('upload.html',UPfiles=UPfiles, DWfiles=DWfiles)
    return render_template('__init__.html')


@app.route('/action', methods=['GET', 'POST'])
def action():
    global email, bar
    if request.method == 'POST':
        user_answer=request.form.get('activity')
        if user_answer == "0":
            UPfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/upload".format(bar[:-1],email))
            DWfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email))
            return render_template('upload.html', UPfiles=UPfiles, DWfiles=DWfiles)
        elif user_answer == "1":
            UPfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/upload".format(bar[:-1],email))
            DWfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email))
            return render_template('upload.html', UPfiles=UPfiles, DWfiles=DWfiles)
        elif user_answer == None:
            return render_template('success.html')
            

        
@app.route('/download', methods=['GET', 'POST'])
def download():
    global email ,bar 
    if request.method == 'POST':
        u_ans=request.form.get('activity')
        return send_from_directory(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email), u_ans, as_attachment=True)
        

@app.route('/upload', methods=['GET', 'POST'])
def index():
    
    global email, bar
    if request.method == 'POST':
        if 'f' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['f']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            now = datetime.now()
            bar1 = now.strftime("[%d-%m-%Y_%H.%M.%S]")
            filename = bar1+" " + filename
            xx=app.config['UPLOAD_FOLDER']
            if "file_by_whome.txt" in os.listdir():
                pass
            else:
                my_file = open("file_by_whome.txt","+a")
                my_file.write("login;name;filename;path\n")
                my_file.close()
            file.save(os.path.join(xx+r"/{}@@{}/upload".format(bar[:-1],email), filename))
            file_name_path = os.path.join(xx+r"/{}@@{}/upload".format(bar[:-1],email), filename)
            print(file_name_path)
            my_file = open("file_by_whome.txt","+a")
            my_file.write(email+";"+bar[:-1]+";"+filename+";"+os.path.join(xx+r"/{}@@{}/upload".format(bar[:-1],email), filename)+"\n")
            my_file.close()
            program_select = request.form.get("program_select")
            global c += 1
            if program_select == "bipartiteLinearKit.py":
                no_below = request.form.get("no_below")
                clm_1 = request.form.get("clm_1")
                clm_2 = request.form.get("clm_2")
                p_core = request.form.get("p_core")
                if no_below == "_" or clm_1 == "_" or clm_2 == "_" or p_core == "_":
                    UPfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/upload".format(bar[:-1],email))
                    DWfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email))
                    os.remove(file_name_path)
                    return render_template('upload.html',UPfiles=UPfiles, DWfiles=DWfiles)
                command=str(program_select)+" "+str(no_below)+" "+str(file_name_path)+" "+str(clm_1)+" "+str(clm_2)+" "+str(p_core)
                Thread(target=run_prog(command,bar[:-1],email,filename,c,)).start()

            elif program_select == "extractPrefix.py":
                prefix = request.form.get("prefix")
                if prefix == "_":
                    UPfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/upload".format(bar[:-1],email))
                    DWfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email))
                    os.remove(file_name_path)
                    return render_template('upload.html',UPfiles=UPfiles, DWfiles=DWfiles)
                command=str(program_select)+" "+str(file_name_path)+" "+str(prefix)
                Thread(target=run_prog(command,bar[:-1],email,filename,c,)).start()

            elif program_select == "orderCommunity.py":
                command=str(program_select)+" "+str(file_name_path)
                Thread(target=run_prog(command,bar[:-1],email,filename,c,)).start()

            else:
                UPfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/upload".format(bar[:-1],email))
                DWfiles=os.listdir(r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download".format(bar[:-1],email))
                return render_template('upload.html',UPfiles=UPfiles, DWfiles=DWfiles)
            command = r""
            return render_template('success.html')
    return render_template('__init__.html')


def run_prog(command,bar,email,filename,c):
    os.system(r"mkdir {}".format(email+str(c)))
    command = command +" "+ str(email)
    pyt = "python "+ str(command)
    os.system(pyt)
    zf = zipfile.ZipFile(r"{}.zip".format(str(filename)), "w")
    for dirname, subdirs, files in os.walk(str(email+str(c))):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    os.rename(r"{}.zip".format(str(filename)),
              r"/home/satyanveshi/zpractice/abhisir web/ABHISHEK_TEST_FINAL/jay_abhi/upload/{}@@{}/download/{}.zip".format(bar,email,str(filename)))
    os.remove(email+str(c))

@app.route('/new_acc', methods=['GET', 'POST'])
def acc_creat():
    global email , password, name
    name = request.form.get('Name')
    email = request.form.get('Email')
    password = request.form.get('Password')
    x=os.listdir("upload")
    folder = ["upload", "download"]
    if name in x:
        pass
    else:
        print("making dir")
        os.mkdir(f"upload/{name}@@{email}")
        for i in folder:
            os.mkdir(f"upload/{name}@@{email}/{i}")
    f=open("members.txt","r")
    for i in f:
        if email in i.split(";")[0]:
            if password in i.split(";")[1]:
                bar = i.split(";")[2]
    if email == "_" or password == "_" or name == "_":
        return render_template('__init__.html')
    my_file = open("members.txt","a")
    my_file.write(email+";"+password+";"+name+"\n")
    return render_template('__init__.html')

if __name__ == '__main__':
    app.run( threaded =True)

