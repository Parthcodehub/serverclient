
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import time
import pickle,socket,random


HOST=socket.gethostname()
ip=socket.gethostbyname(HOST)
#ip="192.168.0.105"
print(HOST+':'+ip)
PORT=9999
global s
s=socket.socket()
#ip=input("Enter the IP of SERVER:")
try:
    s.connect((ip,PORT))
except Exception as e:
    print("\nINVALID IP ")
    print(e)
    time.sleep(4)
    exit(0)
form_class = uic.loadUiType("parallel.ui")[0]
#form_classs = uic.loadUiType("MainUi.ui")[0]

class loginform(QtWidgets.QMainWindow,form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        try:
            self.p1.clicked.connect(self.pf1)
            self.p2.clicked.connect(self.pf2)
            self.p3.clicked.connect(self.pf3)
            self.p4.clicked.connect(self.pf4)
        except Exception as e:
            print(e)
    def sender(self,query):
        print("in")
        data1 = pickle.dumps(query)
        s.send(data1)
        datar1 = s.recv(1024)
        datal1 = pickle.loads(datar1)
        s.send(data1)
        data2 = s.recv(datal1)
        datarescan = pickle.loads(data2)
        print(datarescan)
    def pf1(self):
        query="SELECT * FROM inn "
        print(query)
        self.sender(query)
        pass
    def pf2(self):
        self.pe2.setText(str(self.rg()))

    def rg(self):
        size = 3
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        j = ''.join(random.choice(chars) for x in range(size))
        co = "select * from inn"
        data1 = pickle.dumps(co)
        s.send(data1)
        datar31 = s.recv(1024)
        datal31 = pickle.loads(datar31)
        s.send(data1)

        data2 = s.recv(datal31)
        tt = pickle.loads(data2)

        # self.cursor.execute(co)
        print()
        print(j)
        # tt=self.cursor.fetchall()
        for gh in tt:
            if str(gh[1])[2:] == str(j):
                print("found")
                # time.sleep(1)
                return self.rg()
        return j
    def pf3(self):
        pass
    def pf4(self):
        pass
app = QtWidgets.QApplication(sys.argv)
windoww=loginform(None)
windoww.show()
app.exec_()
