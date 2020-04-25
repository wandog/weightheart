#!/usr/bin/python
#coding:utf-8
#from sys import argv
import zbar
from selenium import webdriver
import os
from selenium.webdriver import chrome
import time 
from selenium.webdriver.common.keys import Keys #for current url
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import sys
import socket
import threading
import sqlite3
from ilock import ILock
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException

reload(sys)
sys.setdefaultencoding('utf-8')


options=webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

#driver = webdriver.Chrome (chrome_options=options)
driver=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)
#driver=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

driver.get ( "http://localhost:5000/index" )

time.sleep(1)

#proc=zbar.Processor()
#proc.parse_config('enable')
#device='/dev/video3'
#proc.init(device)
#proc.visible=True
#################################
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(('192.168.1.123', 54321))

lock=threading.Lock()

##################################
######################################

#thread to run automation member check in
def automation():
    global proc
    global sock
    global driver
    while True:
        
        
        #proc.process_one()
            
        fp=open("/dev/ttyACM0",'rb')
        #while True:
        fp.flush()
        text=fp.read(5)
        fp.close()
                #break

        print "text is "+text


        #for symbol in proc.results:
        #    print 'decoded', symbol.type, 'symbol', '"%s"' %symbol.data
        #    print symbol.data
        
        driver.get ( "http://localhost:5000/index" )
        time.sleep(1)       

        #text=symbol.data

        if (text[0] =="m") is not True:
            continue

        driver.find_element_by_id("memberID").clear()
        driver.find_element_by_id("memberID").send_keys(text)
        time.sleep(0.5)
        print "input data is "+text     
        continue

        click_able=driver.find_element_by_id("btnGetIn")

        if click_able.is_enabled()==True:
            time.sleep(0.5)
            driver.find_element_by_id("btnGetIn").click()
            print "btnGetIn is clicked"
        else:
            continue

        lock.acquire()
        print "lock acquire in automation"
        close_btn=driver.find_element_by_id("close_1")
        print "get dom of modal close btn"
        
        # count_1=0
        while True:
            if close_btn.is_displayed():
                print "close btn is displayed"
                time.sleep(0.5)
                response=driver.find_element_by_id("response_1").text
                break
            else:
                pass
        
        

        # try:
        if "沒有購買" in response or "無有效" in response:
            driver.find_element_by_id("close_1").click()    #close modal dialog
            time.sleep(0.5)
            driver.find_element_by_id("btnGetInTimes").click()  #check times contract
            time.sleep(0.5)
            msg="need confirm for decrease times contract"
            sock.send(msg)
            time.sleep(0.5)
            feedback=sock.recv(1024)
            print feedback
            #decide accept or dismiss for times member
            if "yes" in feedback:
                driver.switch_to_alert().accept()
                time.sleep(0.5)
                while True:
                    if close_btn.is_displayed():
                        time.sleep(0.5)
                        response=driver.find_element_by_id("response_1").text
                        break
                    else:
                        pass
                    # count_1=count_1+1
                    # if(count_1>1000):
                    #     print "timeout for wait modal"
                    #     count_1=0
                    #     break
                # print response
                #time.sleep(0.5)
                sock.send(response) #send the content of dialog 
                time.sleep(0.5)
            elif "no" in feedback:
                driver.switch_to_alert().dismiss()
            else:
                print "return msg not yes or no"
        elif "會籍" in response:
            #time.sleep(0.5)
            sock.send(response)
            time.sleep(1)
        else:   #show bulletin
            print ("no expected response is saw!")
                
        # except:
        #     print("automation control err happened and rescan qrcode please!!")
        
        print "lock release in automation"
        #time.sleep(2)
        lock.release()



#thread for send bulletin

def showBulletin():
    global sock
    
    count=0
    msg=""
    
    #conn = sqlite3.connect('./web_flask/test.db')
    #print "Opened database successfully"
    
    while True:
        #with ILock('gym'):
        conn = sqlite3.connect('./web_flask/test.db',timeout=20.0)
        with conn:
            print "Opened database successfully"
            result=conn.execute("select content from bulletin where b_num=?",((count%3)+1,)).fetchone()
        
            print result[0]
            msg=result[0]
            print msg
        
        
        #the msg should be read from db
        lock.acquire() 
        sock.send("bulletin"+msg)
        lock.release()
        
        
        count=count+1
        time.sleep(10)
        
    #conn.close()
t1=threading.Thread(target=automation)
#t2=threading.Thread(target=showBulletin)

t1.start()
#t2.start()

t1.join()
#t2.join()


#sock.close()
    


