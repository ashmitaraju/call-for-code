from app import app
from flask import Flask, render_template,request, Response, url_for,flash, redirect
from flask_login import login_user, login_required,current_user, logout_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app import conn
import ibm_db
import os

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=fkk32348;PWD=kzpx8xvfvg-4642k","fkk32348","kzpx8xvfvg-4642k")

@app.route('/')
def index():
    return render_template('index.html',title='ISL | Home')

@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')

@app.route('/satellite')
def satellite():
    return "satellite"

@app.route('/inventory')
def inventory():

    stmt = ibm_db.exec_immediate(conn, "UPDATE SURVEY SET LAT=34.55 WHERE id = 1")
    return "inventory"

@app.route('/heatmap')
def heatmap():
    return "heatmap"


#######Prevents cacehing of static files in the browser#######
@app.context_processor
#@cross_origin(supports_credentials=True)
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
##############################################################
