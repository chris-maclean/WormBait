#!/usr/bin/python
import os
import sys

majorVersion = sys.version_info[0]
folder = ""
if majorVersion == 3:
	folder = "python3"
elif majorVersion == 2:
	folder = "python2"

if folder:
	here = os.path.dirname(os.path.realpath(__file__))
	print("Running " + folder + "/wormbait.py")
	os.system("python " + str(here) +"/" + folder + "/wormbait.py")
else:
	print("WormBait could not determine your installed Python version")
	

    
