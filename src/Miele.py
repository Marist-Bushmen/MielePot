#!/usr/bin/python3
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta, time, date
import os.path, dbHelper, sendToQueue


MielePot = Flask(__name__)

#Global vars
apiAbbr    = "MIE"
apiVersion = "02"
ID = apiAbbr+apiVersion
apiName = "Website Admin System v" + apiVersion
apiPort = 4400
HPID = os.environ['HPID']


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
        dbHelper.insertIntoDB(uname, passw, str(fromIP))

        if str(request.form.get('username')) == 'admin' and str(request.form.get('password')) == 'admin':
            return render_template('data.html', data=dbHelper.getData('SELECT * FROM data;'))
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
    ID + ',' + str(datetime.now()) + ',' + hostIP + ','+ hostName + ','
    + str(os.getpid()) + ',' + HPID + ',' + log + '\n'
    )

    #Log activity
    filename = ID + '-' + str(datetime.today().date()) + '.log'

    
    log_dir = 'logs/'
    try:
        os.stat(log_dir)
    except:
        os.mkdir(log_dir)  

    # Append to file or create a new one if it is a new day
    file = open(log_dir+filename, 'a+')
    
    # If its a new file write a header
    if os.stat(log_dir+filename).st_size == 0:
        file.write(logHeader)
        
        # Change to the log dir and count the number of logs
        os.chdir(log_dir)    
        file_count = len([name for name in os.listdir(".")])
     
        # If there are more than 10 files delete the oldest
        if file_count > 10:
            oldest_file = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)[0]
            print('-------------removing' + oldest_file)
            os.remove(oldest_file)

        # Change back to the original directory
        os.chdir('..')    


    #Send to Message Queue
    sendToQueue.sendMsg(logEntry)

    # Write the log entry
    file.write(logEntry)
    file.close()



if __name__ == '__main__':
    MielePot.run(host='0.0.0.0', port=apiPort,debug=True)
