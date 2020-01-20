#!/usr/bin/python

import os
import time
import sys

BACKUP_PATH = '/media/ezrama/bakup_disk/'


current_time= time.time()
try:
    for f in os.listdir(BACKUP_PATH):
        print(f)
        creation_time = os.path.getctime(BACKUP_PATH+f)
        days=(current_time - creation_time) // 86400
        print(days)
        if days>=7: #over 7 days
            print(BACKUP_PATH+str(f))
            os.unlink(BACKUP_PATH+str(f))
            print('{} removed'.format(f))
except:
    print("no need to del old bak files")

print("del script exit")
