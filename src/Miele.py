#!/usr/bin/python3
# Author: Daniel N. Gisolfi
# Purpose: Define all routes in the miele Honeypot, log all attacks
# Date: 2018-10-05

import os.path
import dbHelper
from datetime import datetime, timedelta, time, date
from flask import Flask, render_template, jsonify, request

miele = Flask(__name__)

#Global vars
api_abbr    = 'MIE'
api_version = '02'
ID = api_abbr + api_version
api_name = 'Website Admin System v' + api_version
api_port = 4400
pot_name = 'miele'
HPID = os.environ['HPID']

@miele.route('/', methods=['GET', 'POST'])
def login():
         
    if request.method == 'POST':
        uname = cleanse(str(request.form.get('username')))
        passw = cleanse(str(request.form.get('password')))

        post_data = 'Username=' + uname + '&Password=' + passw
        post_data = cleanse(post_data)

        # Record attempt in database
        from_ip = createLog(post_data)
        dbHelper.insertIntoDB(uname, passw, from_ip)
        

        if uname == 'admin' and passw == 'admin':
            return render_template('data.html', data=dbHelper.getData('SELECT * FROM data;'))
        else:
            return render_template(
            'login.html',
             error='Incorrect Username or Password, please try again')
    else:       
        # If no post data fill the field will be null
        createLog('null')
        
        return render_template('login.html')
    

# Clean all log inputs of any dangerous characters
def cleanse(input):
    output = input.replace(',','COMMA')
    output = output.replace('\\','BSLASH')
    return output


def createLog(post_text):
    
    global api_port
    # All honeypots should have these columns
    logHeader = 'ID,Timestamp,hostIP,hostName,hostPID,HPID,method,requestedText,sourceIP,sourcePort,userAgent,text\n'

    # Get the hostname of the server
    try:
        host_name = os.environ['USER']
    except:
        try:        
            host_name = os.environ['HOSTNAME']
        except:
            host_name = 'NOT FOUND'   
   
    # Declearing all the fields and cleansing the data
    timestamp = str(datetime.now())
    host_ip = cleanse(str(request.host).split(':')[0])
    host_name = cleanse(host_name)
    host_pid = str(os.getpid())
    method = cleanse(str(request.method))
    req_text = cleanse(str(request.path))
    from_ip = cleanse(str(request.environ['REMOTE_ADDR']).split(':')[0])
    api_port = str(api_port)
    user_agent = cleanse(str(request.headers.get('User-Agent')))
    text = cleanse(post_text)
 

    # Create an entry
    log = (ID + ',' + timestamp + ',' + pot_name + ',' + host_ip + ',' + host_name + ','
    + host_pid + ',' + HPID + ',' + method + ',' + req_text + ',' 
    + from_ip + ',' + api_port + ',' + user_agent + ',' + text + '\n')

    # Create a new file everyday
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
        file_count = len([name for name in os.listdir('.')])
     
        # If there are more than 10 files delete the oldest
        if file_count > 10:
            oldest_file = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)[0]
            print('-------------removing' + oldest_file)
            os.remove(oldest_file)

        # Change back to the original directory
        os.chdir('..')    
   
    # Write the log entry
    file.write(log)
    file.close()

    return from_ip
                      

if __name__ == '__main__':
    miele.run(host='0.0.0.0', port=api_port, debug=True)
