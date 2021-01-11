'''import socket
import argparse
import threading
import pickle
from PyQt5.QtCore import QThread
import pymysql, time

parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")
sck = socket.socket()
# sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

global c,ip
global cursor
try:
    db = pymysql.connect(host="localhost", user="root", password="", database="sci")
    cursor = db.cursor()
    print("DATABASE CONNECTED")
except Exception as e:
    print(e)

try:
    sck.bind((args.host, args.port))
    sck.listen(10)
except Exception as e:
    raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")

class new(QThread):
    def run(self):
        print("here")

        try:
            print(c,ip)
        except Exception as e:
            print(e)
        new.conn(c)
    def conn(c):
        i=[0,2,3,4,5]
        while True:  # infinite loop hearing for query request from client
            recd = c.recv(10240)
            query = pickle.loads(recd)
            # print(type(query))
            print(i[1], ':>', query)
            if query.startswith('CREATE') or query.startswith('UPDATE') or query.startswith(
                    'INSERT') or query.startswith('DELETE') or query.startswith('DROP'):
                # print('no update in table has done')
                fnum = 1024
                ldata = pickle.dumps(fnum)
                c.send(ldata)

            else:
                print(c, ip)
                cursor.execute(query)
                # db.commit()
                result1 = cursor.fetchall()
                # data=pickle.dumps(result1)
                data = pickle.dumps(result1)
                length = len(data)
                # print("length req:",length)
                ldata = pickle.dumps(length)
                c.send(ldata)

            recd = c.recv(10240)
            query = pickle.loads(recd)
            print(i[1], ':>', query)
            cursor.execute(query)
            db.commit()
            result1 = cursor.fetchall()
            data = pickle.dumps(result1)
            c.send(data)


        # fuction call to another file of loginsocket_server


while True:
    try:
        c, ip = sck.accept()
        #threading._start_new_thread(on_new_client,(c, ip))  # ip contains ipaddress and port of the client
        f=new()
        f.start()
    except KeyboardInterrupt:
        print(f"Gracefully shutting down the server!")
    except Exception as e:
        print(f"Well I did not anticipate this: {e}")
sck.close()'''
import socket
import argparse
import threading
import pickle

import pymysql, time

parser = argparse.ArgumentParser(description="This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=9999)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")
sck = socket.socket()
# sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

global c
global cursor
try:
    db = pymysql.connect(host="localhost", user="root", password="", database="sci")
    cursor = db.cursor()
    print("DATABASE CONNECTED")
except Exception as e:
    print(e)

try:
    sck.bind((args.host, args.port))
    sck.listen(10)
except Exception as e:
    raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")


def conn(c):
    i=[0,12,3,4,5]
    while True:  # infinite loop hearing for query request from client
        recd = c.recv(10240)                                                            #query received from client side
        query = pickle.loads(recd)
        # print(type(query))
        print(i[1], ':>', query)
        if query.startswith('CREATE') or query.startswith('UPDATE') or query.startswith(
                'INSERT') or query.startswith('DELETE') or query.startswith('DROP'):
            # print('no update in table has done')
            fnum = 1024
            ldata = pickle.dumps(fnum)
            c.send(ldata)                                                               #output send to client

        else:
            cursor.execute(query)
            # db.commit()
            result1 = cursor.fetchall()
            # data=pickle.dumps(result1)
            data = pickle.dumps(result1)
            length = len(data)
            # print("length req:",length)
            ldata = pickle.dumps(length)
            c.send(ldata)                                                                #output send to client

        recd = c.recv(10240)
        query = pickle.loads(recd)
        print(i[1], ':>', query)
        cursor.execute(query)
        db.commit()
        result1 = cursor.fetchall()
        data = pickle.dumps(result1)
        c.send(data)


def on_new_client(c, connection):
    conn(c)
    # fuction call to another file of loginsocket_server


while True:
    try:
        c, ip = sck.accept()
        threading._start_new_thread(on_new_client, (c, ip))  # ip contains ipaddress and port of the client
    except KeyboardInterrupt:
        print(f"Gracefully shutting down the server!")
    except Exception as e:
        print(f"Well I did not anticipate this: {e}")
