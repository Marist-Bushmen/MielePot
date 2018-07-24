#!/usr/bin/python3
import os, json, psycopg2

#Create db login credentials
db_login = {
  'database': 'miele',
  'user': 'miele',
  'password': 'bigCh0ke',
  'host': 'db',
  'port': 5432
}


def runQuery(conn, cur, query):
    cur.execute(query)
    print(cur.fetchall())

def connectDB():
    conn = psycopg2.connect(**db_login)
    #Connect with pyscopg2
    cur = conn.cursor()
    return conn, cur

def getData(query):
    conn, cur = connectDB()
    cur.execute(query)
    attempts = []
    for entry in cur.fetchall():
        descr = entry[1]
        uname = entry[2]
        pwd = entry[3]
        attempts.append({'descr': descr, 'uname': uname,'pwd': pwd})
    return attempts


def insertIntoDB(username, password, ip_address):
    # try:
    conn = psycopg2.connect(**db_login)
    #Connect with pyscopg2
    cur = conn.cursor()
    cur.execute("INSERT INTO loginattempts" +"(username, password, ip_address) VALUES(%s,%s,%s)",
    (username, password, ip_address))
    conn.commit()
    # except:
    #     raise ValueError('ERR INSERT FAILED')
