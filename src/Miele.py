#!/usr/bin/python3
from flask import Flask, render_template, jsonify, request
from datetime import date, datetime, timedelta
import os.path, DB


MielePot = Flask(__name__)

#Global vars
apiAbbr    = "MIE";
apiVersion = "02"
ID = apiAbbr+apiVersion
apiName = "Website Admin System v" + apiVersion
apiPort = 4400
HPID = os.environ['HPID']
timestamp = str(datetime.now())


@MielePot.route('/', methods=['GET', 'POST'])
def login():
    #get sddress of the container or vm As well as from the user
    hostIP = request.remote_addr
    fromIP = request.environ['REMOTE_ADDR']


    if request.method == "POST":
        uname = str(request.form.get('username')).replace(',','COMMA')
        passw = str(request.form.get('password')).replace(',','COMMA')

        #if user posted data get uname and pw
        postData = 'Username=' + uname + '&Password=' + passw

        #create a log of post data
        log = (str(request.method) + ',' + request.path + ','
        + str(fromIP) + ',' + str(apiPort)
        + ',' + str(request.headers.get('User-Agent')) + ',' + postData)
        createLog(log, hostIP)

        #record attempt in database
        DB.insertIntoDB(uname, passw, str(fromIP))

        if str(request.form.get('username')) == 'admin' and str(request.form.get('password')) == 'admin':
            return render_template('data.html', data=DB.getData('SELECT * FROM data;'))
        else:
            return render_template(
            'login.html',
             error="Incorrect Username or Password, please try again")
    else:
        #create a log of post data
        log = (str(request.method) + ',' + request.path + ','
        + str(fromIP) + ',' + str(apiPort)
        + ',' + str(request.headers.get('User-Agent')))
        createLog(log, hostIP)

        return render_template('login.html')



def createLog(log, hostIP):
    logHeader = 'ID,Timestamp,hostIP,hostName,hostPID,HPID,method,requestedText,sourceIP,sourcePort,userAgent,text\n'
    #PEI02,2018-07-20T17:38:55.316,172.17.0.2,351b872c1952,5,abcecc0f27f63ba841c5a5575b520302,POST,/listDIR,148.100.133.128,80,Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:61.0) Gecko/20100101 Firefox/61.0,username=admin,password=admin
    #Make sure you get the HOSTNAME
    try:
        hostName = os.environ['USER']
        getHostName = True
    except:
        getHostName = False

    if getHostName == False:
        try:
            hostName = os.environ['HOSTNAME']
        except:
            getHostName = False
    else:
        hostName = 'NOT FOUND'

    #Finish the log file
    logEntry = (
    ID + ',' + timestamp + ',' + hostIP + ','+ hostName + ','
    + str(os.getpid()) + ',' + HPID + ',' + log + '\n'
    )

    #Log activity
    filename = ID + '.log'
    if os.path.exists(filename):
        yesterday = (datetime.now() - timedelta(days=1))
        file_date = datetime.fromtimestamp(os.path.getctime(filename)).day

        if file_date <= yesterday.day:
           os.rename(ID + '-'+ str(yesterday.date()) + '.log')

        #append to file
        file = open(filename, 'a')

    else:
        #create new file
        file = open(filename, 'w')
        file.write(logHeader)

    file.write(logEntry)
    file.close()



if __name__ == '__main__':
    MielePot.run(host='0.0.0.0', port=apiPort)
