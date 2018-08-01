#!/usr/bin/python3
import pika

host = '10.11.17.26'

def connect():
    #For local host use: connection = pika.BlockingConnection(pika.ConnectionParameters(host='NAME OF CONTAINER'))
    parameters = pika.URLParameters('amqp://admin:bigchoke@' + host +':5672/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='honeynet')
    return connection, channel

def sendMsg(payload):
    try:
        connection, channel = connect()
    except pika.exceptions.AMQPConnectionError:
        print("connection failed")

    try:
        channel.basic_publish(exchange='', routing_key='honeynet', body=payload)
        print('Sending: \n' + payload + '\nTo: honeynet')
        connection.close()
    except:
        print("Publishing error")
