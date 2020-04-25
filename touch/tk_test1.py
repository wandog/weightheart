#!/usr/bin/python
#coding:utf-8
import sys
from Tkinter import *
import threading
import time
import socket
import textwrap
import tkFont as font
import MySQLdb as mariadb
#import sqlite3


reload(sys)
sys.setdefaultencoding('utf-8')

flag_answer=False
flag_wait_input=False
flag_alive=True
lock=threading.Lock()
lock_1=threading.Lock()

def normalizeMsg(msg):
    msg=msg.replace("bulletin","",1)
    msg=textwrap.fill(msg,width=48)
    #print msg
    return msg

def get_db():
    # global dbq
    # db = getattr(g, '_database', None)
    # if db is None:
    mariadb_connection = mariadb.connect(host='localhost',user='wandog', passwd='q0919155809', db='weightheart',charset="utf8")
    return mariadb_connection
        



dataShow=normalizeMsg("重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房")

def showBulletin():
    global dataShow
    db=get_db()
    count=0
    count_1=0
    while True:
        with db:
        
            cursor=db.cursor()
            count_1=count/100
            count=count+1
            # count_1=count_1+1
            cursor.execute("select content from bulletin where b_num=%s",(count_1%3+1,))
        
            result=cursor.fetchone()
            lock.acquire()
            dataShow=result[0]
            lock.release()
            #print "thread bulletin: "+result[0]+" and count_1: "+str(count_1)
            time.sleep(0.1)

#def watchdog_connection():
#    global flag_alive 
#    sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    sock_1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
#    sock_1.bind(('0.0.0.0', 54322))
#    sock_1.listen(10)
#    (csock_1, adr_1) = sock_1.accept()

#    while True:
#        try:
#            csock_1.send("alive test")
#            flag_alive=True
#        except:
#            print "client crash!!"
#            flag_alive=False
#            print "flag_alive is false"
#            csock_1.close()
#            sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            sock_1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
#            sock_1.bind(('0.0.0.0', 54322))
#            sock_1.listen(10)
#            (csock_1, adr_1) = sock_1.accept()
#            print "reset complete for watchdog" 
#        time.sleep(1)


def socket_server():
    # global csock
    global dataShow
    global flag_answer
    global flag_wait_input
    global flag_alive
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
    sock.bind(('0.0.0.0', 54321))
    sock.listen(10)
    (csock, adr) = sock.accept()
    #csock.setblocking(0)
    #print "Client Info: ", csock, adr
    while True:
        
        try:
            msg=csock.recv(1024)
        except:
            #if flag_alive is not True:
            print "client crash and reset socket"
            csock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
            sock.bind(('0.0.0.0', 54321))
            sock.listen(10)
            (csock, adr) = sock.accept()
            continue
        
        lock.acquire()
        
        if "need confirm" in msg:
                # msg=raw_input("input data:")
            flag_wait_input=True
            
            dataShow="請確認是否要扣儲值次數"
            
            while True:
                lock_1.acquire()
                if flag_wait_input == False:
                    if(flag_answer==True):
                        msg="yes"
                        print "get yes button"
                    else:
                        msg="no"
                        print "get no button"
                    flag_answer=False
                    lock_1.release()
                    break
                lock_1.release()
                time.sleep(1)
            csock.send(msg)

        elif "會籍" in msg or "儲值" in msg:
                # flag_wait_input=True
            temp=normalizeMsg(msg)
            dataShow=temp.replace("此會員","您")
            while True:
                lock_1.acquire()
                if flag_answer == True:
                        # flag_wait_input=False
                    flag_answer=False
                    lock_1.release()
                    break
                lock_1.release()
                time.sleep(1)
            
            #elif "bulletin" in msg:
            #    dataShow=normalizeMsg(msg)
        else:
            print "the msg is not what we needed"
            csock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
            sock.bind(('0.0.0.0', 54321))
            sock.listen(10)
            (csock, adr) = sock.accept()
                #print "Client Info: ", csock, adr
        
        lock.release()
        
        time.sleep(0.1)
    csock.close()



def change_text():
    global flag_wait_input
    global flag_answer
    global mylabel

    mylabel.configure(text=dataShow)
    mylabel.after(500, change_text)
    

def setYes():
    global flag_answer
    global flag_wait_input
    lock_1.acquire()
    flag_answer=True
    flag_wait_input=False
    print "yes"
    lock_1.release()

def setNo():
    global flag_answer
    global flag_wait_input
    lock_1.acquire()
    flag_answer=False
    flag_wait_input=False
    print "no"
    lock_1.release()


window = Tk()
window.title("重心健身房 電子佈告欄")
window.geometry('1280x800')

mylabel =Message(window, text="hello")
mylabel.config(font=('Arial', 40, 'italic'),anchor="center",width=1200)
mylabel.pack()

# mylabel.visible = True
# mylabel.place(x=20, y=50)
# mylabel.pi = mylabel.place_info()
mylabel.after(500, change_text)

# below is about buttons


photoYes = PhotoImage(file = "/home/pi/test_code/touch/yes.png")
btnYes = Button(window,width=200,height=160,bg="green",command=setYes, image=photoYes)
btnYes.place(x=70,y=600)

photoNo = PhotoImage(file = "/home/pi/test_code/touch/no.png")
btnNo = Button(window, text="取消",width=200,height=160,bg="red",command=setNo,image=photoNo)
btnNo.place(x=300, y=600)




t1=threading.Thread(target=socket_server)
t2=threading.Thread(target=showBulletin)
t1.start()
t2.start()
window.mainloop()




# t1.join()

# t2.join()

