from flask import Flask, render_template, jsonify, request
from datetime import date, datetime
import os.path


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
        #if user posted data get uname and pw
        postData = 'Username=' + str(request.form.get('username')) + ',Password=' + str(request.form.get('password'))

        #create a log of post data
        log = (str(request.method) + ',' + request.path + ','
        + str(fromIP) + ',' + str(apiPort)
        + ',' + str(request.headers.get('User-Agent')) + ',' + postData)
        createLog(log, hostIP)

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
    #Make sure you get the HOSTNAME
    try:
        hostName = os.environ['USER']
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
    fileName = 'Miele.log'
    if os.path.exists(fileName):
        #append to file
        file = open(fileName, 'a')
    else:
        #create new file
        file = open(fileName, 'w')

    file.write(logEntry)
    file.close()


if __name__ == '__main__':
    MielePot.run(host='0.0.0.0', port=apiPort)
