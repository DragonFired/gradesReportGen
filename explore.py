#!/usr/bin/env python
__author__ = "Arana Fireheart"

with open("/flash/testRGBLed.py", 'r') as inFile:
     for line in inFile.readlines():
         print(line.rstrip())

exec(open("/flash/testRGBLed.py").read())
exec(open("/flash/testRGBLed.py").read())
