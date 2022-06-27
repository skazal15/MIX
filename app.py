#!/usr/bin/env python
# coding: utf-8

# In[234]:

from datetime import datetime,date
import pandas as pd # Import Pandas for data manipulation using dataframes
import os
from werkzeug.utils import secure_filename
import sys
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, send_file
from analis import all_data, data_all, period, hit
from analis import instances as instances1
app = Flask(__name__,static_url_path='/static')
app.secret_key = 'loginner'
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png','JPG','JPEG','PNG','xlsx'}
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

measure = {'Emas1':'%',
           'SCM':'GB','ERM':'GB','MUF':'GB','AML':'GB','MANDIRI ONLINE':'GB'}
instances = ['Emas1','SCM','ERM','MUF','AML','MANDIRI ONLINE']
intervals = ['Month', 'Day', 'Hour']
users = {'mandiri':'mandiri123','konsolidasi':'konsolidasi123'}
path = ['/u01','/log','/app','/temp']
pasen = [10,20,30,40]




def dashboard():
    key2=[]
    datepred = []
    lastusage = []
    persen = []
    predict = []
    mer = []
    for it in range(0,len(instances)):
        prediction_date = all_data[it][1]
        datepred.append(prediction_date)
        lastusage.append(round(all_data[it][13],2))
        predict.append(round(all_data[it][8],2))
        if measure[all_data[it][7]] != '%':
            persen.append(round(all_data[it][13] / 1000,0))
        if measure[all_data[it][7]] == '%':
            persen.append(round(all_data[it][13]))
        mer.append(measure[all_data[it][7]])
    duedate = datepred[0]
    for it in range(len(instances)):
        if all_data[it][1] == duedate:
            key2 = all_data[it][0]
            prediction_date1=all_data[it][1]
            d = all_data[it][2]
            series1 = all_data[it][3]
            color = all_data[it][4]
            predictiondat1 = all_data[it][5]
            mse = all_data[it][6]
            instance = all_data[it][7]
            predict1 = round(all_data[it][8],2)
            d1 = all_data[it][9]
            predictdat1 = all_data[it][10]
            predictmax = round(max(all_data[it][10]),0)
            predictmin = round(min(predictdat1),0)
    return(datepred,lastusage,key2,d,series1,color,predictiondat1,mse,instance,predict,d1,predictdat1,predictmax,predictmin,persen,prediction_date1,predict1,mer)

@app.route('/', methods=['POST','GET'])
def login():
    session['logged_in'] = False
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password and username in users and users[username] == password or username != None:
        session['logged_in']=True
        session['user']=username
        session['pass']=password
        if username == 'mandiri' or username !=None:
            return redirect(url_for('done'))
        elif username == 'konsolidasi':
            return render_template('vendor.html', show_results="false",instances=instances, instancelen = len(instances), instance="", foldername="",measure="")
    return render_template('login.html')

# In[260]:

@app.route('/done')
def done():
    print(session['logged_in'])
    if session['logged_in'] == 'false' or session['logged_in']=='':
        return redirect(url_for('login'))
    username = str(session.get('user',None))
    datepred,lastusage,key2,d,series1,color,predictiondat1,mse,instance,predict,d1,predictdat1,predictmax,predictmin,persen,due,predict1,mer=dashboard()
    return render_template('index2.html',show_results="false", instancelen = len(instances), instances=instances, key2="",
                    predict=predict, predictmax=predictmax,
                    prediction_date=datepred, dates=d1, color="#4747A1", predictiondat=predictdat1,max=predictmax,min=predictmin, mse=[], instance=instance,usern=username,due=due,lastusage=lastusage,persen=persen,mer=mer)



@app.route('/instance')
def instance():
    datepred,lastusage,key2,d,series1,color,predictiondat1,mse,instance,predict,d1,predictdat1,predictmax,predictmin,persen,due,predict1,mer=dashboard()
    return render_template('instance.html',instancelen=len(instances),instances=instances,prediction_date=datepred,lastusage=lastusage,mer=mer )


@app.route('/user')
# ‘/’ URL is bound with hello_world() function.
def user():
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    # all_files = utils.read_all_stock_files('individual_stocks_5yr')
    # df = all_files['A']
    # # df = pd.read_csv('GOOG_30_days.csv')
    # all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data = perform_training('A', df, ['SVR_linear'])

    return render_template('index.html',show_results="false", instancelen = len(instances), instances=instances, key2="",
                           predict=[],
                           prediction_date="", dates=[], series=[], color="", predictiondat=[], mse=[], instance="", mer = "" )


# In[ ]:


@app.route('/process/<instancen>', methods=['POST','GET'])
def process(instancen):  
    i = instancen
    mer = measure[i]
    for it in range(len(instances)):
        if i == all_data[it][7]:
            key2 = all_data[it][0]
            prediction_date = all_data[it][1]
            d = all_data[it][2]
            series1 = all_data[it][3]
            color = all_data[it][4]
            predictiondat1 = all_data[it][5]
            mse = all_data[it][6]
            instance = all_data[it][7]
            predict = round(all_data[it][8],2)
            d1 = all_data[it][9]
            predictdat1 = all_data[it][10]
    print(len(predictdat1))
    print(len(d1))
    return render_template('proses.html',key2=key2, show_results="true", instancelen = len(instances), instances=instances,
                           mse=mse,
                           predict=predict,
                           prediction_date=prediction_date, dates=d, dates2=d1, series2=predictdat1, series=series1, color=color, predictiondat=predictiondat1, instance=instance,mer=mer)

@app.route('/vendor', methods=['POST','GET'])
def vendor():
    if not session.get('logged_in'):
        return redirect(url_for('login')) 
    return render_template('vendor.html', show_results="false",instances=instances, instancelen = len(instances), instance="", foldername="",measure="")

@app.route('/show', methods=['POST','GET'])
def show():
    i = request.form['instance']
    a = data_all[i]
    p = period[a]
    m = measure[i]
    return render_template('vendor.html', show_results="show",instances=instances, instancelen = len(instances), instance=i, interval=p, intervallen=len(intervals), invervals=intervals, foldername=a, measure=m)

@app.route('/edit')
def edit():
    return render_template('data.html')

@app.route('/add', methods=['POST','GET'])
def add():
    i = request.form['instance1']
    p = request.form['interval1']
    m = request.form['measure']
    if 'file' not in request.files:
        print('No file attached in request')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print('No file selected')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    path =(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    print("path :",path)
    result = path.split("/")
    filename2 = result[-1:]
    print("fname :" ,filename2)
    filename1 = " ".join(filename2)
    if i not in instances:
        instances.append(i)
        instances1.append(i)
    period[filename]=p
    data_all[i]=filename
    measure[i]=m
    print(instances)
    print(instances1)
    print(period)
    print(data_all)
    print(len(instances))
    hit()
    return render_template('data.html', show_results="false",instances=instances, instancelen = len(instances), instance="", foldername="",measure="")

@app.route('/add1', methods=['POST','GET'])
def add1():
    return render_template('vendor.html', show_results="edit",instances=instances, instancelen = len(instances), instance="", intervals=intervals, intervallen=len(intervals), interval="", foldername="", measure="")

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + '/'+filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route('/logout', methods=['POST','GET'])
def logout():
    session['logged_in'] = False
    return render_template('login.html')

@app.route('/storage')
def store():
    paths=[]
    sto=[]
    for i in range(0,len(path)):
        paths.append(path[i])
        sto.append(pasen[i])
    return render_template('prosesstorg.html',paths=paths,sto=sto,storagelen=len(path))

@app.route('/fore')
def fore():
    i = instances[1]
    mer = measure[i]
    for it in range(len(instances)):
        if i == all_data[it][7]:
            key2 = all_data[it][0]
            prediction_date = all_data[it][1]
            d = all_data[it][2]
            series1 = all_data[it][3]
            color = all_data[it][4]
            predictiondat1 = all_data[it][5]
            mse = all_data[it][6]
            instance = all_data[it][7]
            predict = round(all_data[it][8],2)
            d1 = all_data[it][9]
            predictdat1 = all_data[it][10]
    print(len(predictdat1))
    print(len(d1))
    return render_template('forecasto.html',key2=key2, show_results="true", instancelen = len(instances), instances=instances,
                           mse=mse,
                           predict=predict,
                           prediction_date=prediction_date, dates=d, dates2=d1, series2=predictdat1, series=series1, color=color, predictiondat=predictiondat1, instance=instance,mer=mer)



@app.route('/tes')
def tes():
    tes=request.args.get('result')
    print(tes)
    return render_template('login.html')
        

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='localhost',port=5000)

