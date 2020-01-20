#!/usr/bin/python
#coding:utf-8
import sys
from Tkinter import *
import threading
import time
import socket
import textwrap
import tkFont as font
reload(sys)
sys.setdefaultencoding('utf-8')

flag_answer=False
flag_wait_input=False
lock=threading.Lock()

def normalizeMsg(msg):
    msg=msg.replace("bulletin","",1)
    msg=textwrap.fill(msg,width=48)
    print msg
    return msg

dataShow=normalizeMsg("重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房重心健身房")


# def toggle():
#     if mylabel.visible:
#         # btnToggle["text"] = "Show Example"
#         # print "Now you don't"
#         mylabel.place_forget()
#     else:
#         mylabel.place(mylabel.pi)
#         print "Now you see it"
#         btnToggle["text"] = "Hide Example"
#     mylabel.visible = not mylabel.visible

def socket_server():
    global csock
    global dataShow
    global flag_answer
    global flag_wait_input
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
    sock.bind(('0.0.0.0', 54321))
    sock.listen(1)
    (csock, adr) = sock.accept()
    print "Client Info: ", csock, adr
    while True:
        msg = csock.recv(1024)
        if not msg:
            pass
        else:
            print "Client send: " + msg
            
            if "need confirm" in msg:
                # msg=raw_input("input data:")
                flag_wait_input=True
                dataShow="請確認是否要扣儲值次數"
                while True:
                    if flag_wait_input == False:
                        if(flag_answer==True):
                            msg="yes"
                        else:
                            msg="no"
                        flag_answer=False
                        break
                    time.sleep(0.1)
                csock.send(msg)
            elif "bulletin" in msg:
                # print "get in bulletin"
                # lock.acquire()
                dataShow=normalizeMsg(msg)
                # print dataShow
                # lock.release()    
            elif "會籍" in msg or "儲值" in msg:
                # flag_wait_input=True
                temp=normalizeMsg(msg)
                dataShow=temp.replace("此會員","您")
                while True:
                    if flag_answer == True:
                        # flag_wait_input=False
                        flag_answer=False
                        break
                    time.sleep(0.1)
                
            else:
                print "the msg is not what we needed"

        time.sleep(1)
    csock.close()



def change_text():
    global flag_wait_input
    global flag_answer
    global mylabel
    # print "get in change text"
    # while True:
    print dataShow

    mylabel.configure(text=dataShow)
        # print "set label text to be %s"%dataShow
        # if flag_wait_input == False:
        #     break
        # time.sleep(1)
    mylabel.after(500, change_text)
    

def setYes():
    global flag_answer
    global flag_wait_input
    flag_answer=True
    flag_wait_input=False
    print "yes"

def setNo():
    global flag_answer
    global flag_wait_input
    flag_answer=False
    flag_wait_input=False
    print "no"


window = Tk()
window.title("重心健身房 電子佈告欄")
window.geometry('1280x800')

# mylabel =Message(window, text="hello",font=('Arial', 50),width=1000)
mylabel =Message(window, text="hello")
mylabel.config(font=('Arial', 40, 'italic'),anchor="nw",width=1200)
mylabel.pack()

# mylabel.visible = True
# mylabel.place(x=20, y=50)
# mylabel.pi = mylabel.place_info()
mylabel.after(500, change_text)

# below is about buttons

# frame = Frame(window, height="200", width="200", bg="green")
# frame.pack()

photoYes = PhotoImage(file = "yes.png")
# btnYes = Button(window, text="確認",width=20,height=6,bg="green",command=setYes, image=phto)
btnYes = Button(window,width=200,height=160,bg="green",command=setYes, image=photoYes)
# btnYes.configure(bd=-2)
btnYes.place(x=70,y=600)
# btnYes.config(font=('helvetica', 20, 'underline italic'))
# myFont = font.Font(size=20)
# btnYes['font']=myFont

photoNo = PhotoImage(file = "no.png")
btnNo = Button(window, text="取消",width=200,height=160,bg="red",command=setNo,image=photoNo)
btnNo.place(x=300, y=600)




t1=threading.Thread(target=socket_server)
t1.start()
window.mainloop()




# t1.join()

# t2.join()

