from flask import Flask, render_template, jsonify, request
from datetime import date, datetime
import os.path


MielePot = Flask(__name__)

#Global vars
apiVersion = "1.00"
apiName = "REST-API v" + apiVersion
apiPort = 5000
currDate = str(date.today())
currTime = datetime.now().strftime('%H:%M:%S')
dateTime = str(datetime.now())

def getHeaders(header):
    if header == 'visitorIP':
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            visitorIP = request.environ['REMOTE_ADDR']
        else:
            #If app behind a proxy
            visitorIP = request.environ['HTTP_X_FORWARDED_FOR']
        return visitorIP

    elif header == 'userAgent':
        userAgent = request.headers.get('User-Agent')
        return userAgent

    elif header == 'method':
        method = request.method
        return method

    elif header == 'command':
        command = request.script_root + request.path
        return command

    elif header == 'all':
        data = request.headers
        for s in data:
            s = str(s)
        return data

    elif header == 'files':
        files = str(request.files)
        return files

    else:
        return 'err please specify header'

def apiHelp():
    help = ("API commands: GET [action], PUT [action], POST [action], DELETE [action]\n\n"
    + "+-- GET  /ver[sion]                          - API version\n"
    + "+-- GET  /date                               - current date\n"
    + "+-- GET  /time                               - current time\n"
    + "+-- GET  /datetime                           - current date and time\n"
    + "+-- GET  /search                             - find files within system\n"
    + "+-- GET  /login                              - login to admin system\n"
    + "\n"
    + "+-- POST \n"
    + "\n"
    + "+-- PUT \n"
    + "\n"
    + "+-- DELETE \n")
    return help

@MielePot.route('/')
def index():
    visitorLog(getHeaders('command'), getHeaders('visitorIP'), method=getHeaders('method'))
    return render_template(
        'index.html',
        port=apiPort,
        title=apiName,
        heading='Home',
        method=getHeaders('method'),
        command=getHeaders('command'),
        Help=apiHelp(),
        headers=getHeaders('all'),
        files=getHeaders('files')
    )

@MielePot.route('/<path:path>', defaults={'path': ''})
def unknownCMD(path):
    if 'search' in getHeaders('command'):
        return search()
    else:
        #Get Session headers
        errResponse = ('Uknown '+ getHeaders('method')
        + ' from:' + getHeaders('visitorIP') + '~'
        + getHeaders('command') + '~' + getHeaders('userAgent'))

        return render_template(
            'index.html',
            port=apiPort,
            title=apiName,
            heading=errResponse,
            method=getHeaders('method'),
            command=getHeaders('command'),
            Help=apiHelp(),
            headers=getHeaders('all'),
            files=getHeaders('files')
        )



@MielePot.route('/version', methods=['GET', 'POST'])
def version():
    visitorLog(getHeaders('command'), getHeaders('visitorIP'), method=getHeaders('method'))
    return jsonify(
    version=apiVersion
    )

@MielePot.route('/ver', methods=['GET', 'POST'])
def ver():
    visitorLog(getHeaders('command'), getHeaders('visitorIP'), method=getHeaders('method'))
    return jsonify(
    version=apiVersion
    )

@MielePot.route('/date', methods=['GET', 'POST'])
def date():
    visitorLog(getHeaders('command'), getHeaders('visitorIP'), method=getHeaders('method'))
    return jsonify(
    currentDate=currDate
    )

@MielePot.route('/time', methods=['GET', 'POST'])
def time():
    visitorLog(getHeaders('command'), getHeaders('visitorIP'), method=getHeaders('method'))
    return jsonify(
    currentDate=currTime
    )

@MielePot.route('/datetime', methods=['GET', 'POST'])
def datetime():
    visitorLog(getHeaders('command'), getHeaders('visitorIP'), method=getHeaders('method'))
    return jsonify(
    currentDate=dateTime
    )

@MielePot.route('/login', methods=['GET'])
def login():
    return render_template('login.html')



def searchLog(searchEntry):
    fileName = 'searchRecords.log'
    if os.path.exists(fileName):
        file = open(fileName, 'a')
        searchEntry+= '\n'
    else:
        file = open(fileName, 'w')

    file.write(searchEntry)
    file.close()


def visitorLog(command, ipADD, method):
    visitor = ('\nAPI received command:' + '~' + method + '~'
    + command + '~'+ 'from:' + ipADD + '~ at:' + dateTime)

    fileName = 'API.log'
    if os.path.exists(fileName):
        file = open(fileName, 'a')
    else:
        file = open(fileName, 'w')

    file.write(visitor)
    file.close()



def search():
    searchEntry = ('API received command:' + '~' + getHeaders('method')
    + '~' + getHeaders('command') + '~' + 'from:' + getHeaders('visitorIP')
    + '~ at:' + dateTime)
    searchLog(searchEntry)

    return jsonify(
    searchResults = 'null',
    )


if __name__ == '__main__':
    MielePot.run(debug=True, port=apiPort)
