#!/usr/bin/python
import os
import sys

"""This script launches WormBait using the code compiled under Python2 or Python3.

There are small but important differences in the code for Python2 and Python3. In
the interest of cross-platform support, this launcher script determines the version
currently running and launches the appropriate WormBait for it. If the version
cannot be determined, the launcher exits and prints an error message. 

Christopher Anna, 2/18/2016
"""

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
	

    
