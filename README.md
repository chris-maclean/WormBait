# WormBait
An interface to the WormBase API

          /
         ()
         ||
         ||
      __  \\
     /  >   \\
     ||` .-"||".
      \\/  _//. `\
       (  (-'  \  \
        \  )   |  |
         `"   /  /
             /  /         Thanks for using WormBait!
            |  (       _    /
             \  `.-.-.'o`\ /
              '.( ( ( .--'
                `"`"'`

Welcome to WormBait! This program was developed for the Department of Infectious Diseases
at the University of Georgia. It is a very narrow, but effective tool for rapidly collecting
data from the WormBase database using their RESTful API.

RUNNING WORMBAIT
-------------------------------------------------
WormBait is written in 100% Python. To run it, you'll need either Python2 or Python3. The
wormBaitLauncher script is provided to make running WormBait painless to those who don't
know or care which version of Python they have installed on their machine.

If you don't know if you have Python on your machine, perform the following:

1. Open a Terminal or cmd window
2. Run this command:
    `python --version`
    
If Python is installed, you should see a line or two of information about your Python version number (probably
2.7 or 3.x). If you get an error message, you'll need to install Python. Start here: https://www.python.org/downloads/

To run WormBait, open a Terminal or cmd window and navigate to the folder where wormBaitLauncher
resides. Then run the following command:

`./wormBaitLauncher.py`

You should see a line of text that says 'Running pythonX/wormbait.py', where X is either 2 or 3.

At this point, if you see errors, you are probably missing packages in your Python installation. Installing
these packages is outside the scope of this README, but I recommend using pip. Start here:
http://python-packaging-user-guide.readthedocs.org/en/latest/installing/.

The following is a full list of packages used in WormBait (most or all of which may be pre-installed on your machine):
- os
- sys
- json
- requests
- Tkinter
- ScrolledText
- re
- threading
- tkFileDialog
- configParser


USING WORMBAIT
-------------------------------------------------
Using WormBait is simple and easy if you have the requisite materials. Here's what
you'll need to get started:

1. A file created by the CuffLinks analysis tool (http://cole-trapnell-lab.github.io/cufflinks/) or a similar program
This file should have row after row of arbitrary ID numbers, followed by the corresponding WormBase gene ID. Also
in this file should be a column for 'log2(fold_change)'. This file is used to associate values you know to
WormBase gene IDs, and to read the log2(fold_change) value. I refer to this file as the 'database' or 'database file' throughout the program.

2. A list of database IDs for which data should be collected.
These IDs can be as simple as row numbers, or as tool-specific as XLOC_IDs. Perhaps you have identified the IDs that are of interest to you using another tool, like the Venny diagram maker. Regardless of where you got them, you need to know which IDs should have data collected for them.

2b. NB: if you wish only to collect data from WormBase and you KNOW the WormBase gene IDs you are interested in, you
can bypass using a database file and simply put your WormBase gene IDs directly into the input box. WormBait will
recognize what you're doing and won't bother you for a database file.

3. An internet connection
Don't leave home without it!

Enter your list of database IDs in the top textarea of the WormBait window. Then specify the filepath to the
database file in the first filechooser line. 

*** Again -- if you do not have a database file and you already know the WormBase gene IDs that are of interest to you, you can enter those gene IDs into the top textarea and ignore the use of the database file.

Then specify the desired filepath to the output CSV file in the second filechooser line. Finally, press the "Process" button.

You'll see text appear in the bottom textarea informing you of WormBait's progress. If it ever stalls, check
the Terminal/cmd window from which you launched WormBait. Error messages will appear here.

When the bottom textarea informs you that the run is finished, open the output file you specified and inspect
the results. The output will include as much of the following data as is available for each ID you provide:

- Database ID (if using a database file)
- WormBase gene ID
- Fold change value (if using a database file)
- Sequence name
- Protein ID
- Best human ortholog
- Description
- Gene class
- Human orthologs
- Nematode orthologs
- Other orthologs

Voila, you have successfully used WormBait to collect data from WormBase!

Christopher Anna

canna12@gmail.com

2/2016
