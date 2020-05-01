import os
import pathlib
import datetime
import pyqrcode
import png
from pyqrcode import QRCode
from io import BytesIO
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import db_connect, storedata, vlicences, vlicence, eloginact,returnid

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = 'E:/Programming/Ai/Demoproject/Uploadimages'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/ehome")
def ehome():
    return render_template("ehome.html")


@app.route("/enterdata")
def enterdata():
    return render_template("enterdata.html")


@app.route("/licence", methods=['GET', 'POST'])
def licence():
    if request.method == "POST" :
        id=request.form['id']
    elif request.method =="GET":
        id=request.args.get('id')
    data3 = vlicence(id)
    session['id'] = id
    #data = qrcode()
    #print(data)
    return render_template("license.html", userdata=data3)


@app.route("/licences")
def licences():
    data,length1 = vlicences()
    return render_template("licenses.html", userdata=data,num=length1)

@app.route("/qrcode",methods=['GET','POST'])
def qrcodeshow():
    id=request.form['id']
    return render_template("qrcode.html",id=id)


#@app.route("/qrcode", methods=['GET', 'POST'])
def qrcode(id):
    # id=request.args.get('id')
    #id = session['id']
    #if request.method == "POST" :
        #id=request.form['id']
    #data3 = vlicence(id)
    #data = "Name: " + str(data3[0][1]) + "\n" + "Father's Name: " + data3[0][2] + "\n" + "Date Of Birth: " + data3[0][
     #   3] + "\n" + "House No: " + data3[0][4] + "\n" + "Colony: " + data3[0][5] + "\n" + "Location: " + data3[0][
      #         6] + "\n" + "Mandal: " + data3[0][7] + "\n" + "District: " + data3[0][8] + "\n" + "Pin: " + data3[0][
       #        9] + "\n" + "Date Of Issue: " + data3[0][10] + "\n" + "Validity: " + data3[0][11]
    link= "http://127.0.0.1:5000"+url_for("licence",id=id)
    url = pyqrcode.create(link)
    #stream = BytesIO()
    #url.svg("myqr.svg", scale=8)
    filepath=Path("E:\Programming\Ai\Demoproject\Static\myqr"+id+".png")
    url.png(filepath,scale=6)

@app.route("/enter", methods=['GET', 'POST'])
def enter():
    if request.method == 'POST':
        f = request.files['photo']
        g = request.files['usersign']
        h = request.files['authoritysign']
        photoname = secure_filename(f.filename)
        signname = secure_filename(g.filename)
        asignname = secure_filename(h.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], photoname))
        g.save(os.path.join(app.config['UPLOAD_FOLDER'], signname))
        h.save(os.path.join(app.config['UPLOAD_FOLDER'], asignname))
        status = storedata(request.form['name'], request.form['fname'], request.form['dob'], request.form['hno'],
                           request.form['colony'], request.form['location'], request.form['mandal'],
                           request.form['dist'], request.form['pin'], request.form['rta'], photoname, signname,
                           asignname, request.form['ref'], request.form['vtype'], request.form['badge'],
                           request.form['blood'])
        if status == 1:
            id=returnid(request.form['name'])
            ida=str(id)
            qrcode(ida)
            return render_template("ehome.html", m1="Previous registration was successful")
        else:
            return render_template("enterdata.html", m2="Failed")
    else:
        return render_template("enterdata.html")


@app.route("/loginact", methods=['GET', 'POST'])
def logact():
    if request.method == 'POST':

        status = eloginact(request.form['username'], request.form['password'])
        if status:
            return render_template("ehome.html", m1="success")
        else:
            return render_template("login.html", msg="Login Failed")


    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
