#!/usr/bin/python
import subprocess
import datetime
import time
import os
import sys
import threading
from subprocess import call


DATETIME = time.strftime('%Y%m%d-%H%M%S')
BACKUP_PATH = '/media/ezrama/bakup_disk/'


if(os.path.ismount("/media/ezrama/bakup_disk")):
    print("bakup disk is mountted and backup script will be executed!")

else:
    print("bakup disk is not mounted")
    sys.exit()


def tar_www():
    global DATETIME
    global BACKUP_PATH

    PATH = '/var/www/html'

    TAR_CMD_1 = "tar -zcPf " + BACKUP_PATH +'www'+'-' +DATETIME + ".tar " + PATH

    print TAR_CMD_1
    subprocess.call (TAR_CMD_1.split(' '))

def tar_git():
    global DATETIME
    global BACKUP_PATH

    PATH= '/var/lib/gitea'

    TAR_CMD_1 = "tar -zcPf " + BACKUP_PATH +'git'+'-' +DATETIME + ".tar " + PATH

    print TAR_CMD_1
    subprocess.call (TAR_CMD_1.split(' '))

def tar_anjia_samba_folder():
    global DATETIME
    global BACKUP_PATH

    PATH= '/home/ezrama/samba_share'

    TAR_CMD_1 = "tar -zcPf " + BACKUP_PATH +'anjia_samba_folder'+'-' +DATETIME + ".tar " + PATH
    print TAR_CMD_1
    subprocess.call (TAR_CMD_1.split(' '))

def mysql_data_dump():
    global DATATIME
    global BACKUP_PATH
    
    database='--all-databases'                                                                     
                                                                                            
    file = open('/media/ezrama/bakup_disk/database.sql-'+DATETIME, 'w')                                                     
    proc = subprocess.Popen(["mysqldump", "-uroot", "-p1414q0919155809", database],stdout=file)    
    proc.communicate()                                                                             
    file.close() 


t1=threading.Thread(target=tar_www)
t1.start()
t2=threading.Thread(target=tar_git)
t2.start()
t3=threading.Thread(target=tar_anjia_samba_folder)
t3.start()
t4=threading.Thread(target=mysql_data_dump)
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
