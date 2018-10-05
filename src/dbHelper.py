#!/usr/bin/python3
# Author: Daniel N. Gisolfi
# Purpose: to preform all connections and queries to the database
# Date: 2018-10-05

import os, json, psycopg2

#Create db login credentials
db_login = {
  'database': 'miele',
  'user': 'honey',
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
        ip_address = entry[2] 
        uname = entry[3]
        pwd = entry[4]
        attempts.append({'descr': descr, 'ip_address':ip_address, 'uname': uname,'pwd': pwd})
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
