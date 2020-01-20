#!/bin/bash

S=$(ps aux|grep 'python seleniumTest.py'|awk 'NR==1 {print $2}')
echo $S
sudo kill -9 $S
