#!/usr/bin/python

import tkinter
import tkinter.filedialog
import WormCSV
from WormBaitUI import ConsoleBox
from WormBaitUI import ProcessButton
from WormBaitUI import AboutWindow
from configparser import SafeConfigParser


class wormbaitWindow(tkinter.Tk):
    VERSION = "1.0"
    
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.dbFilePath = tkinter.StringVar()
        self.outFilePath = tkinter.StringVar()
        self.entryList = ConsoleBox(self, 10)
        self.protocol("WM_DELETE_WINDOW", self.saveIniAndDestroy)
        self.buildContent()

    def buildContent(self):
        self.parseConfig()
        self.grid()
        
        menubar = tkinter.Menu(self)
        aboutMenu = tkinter.Menu(menubar, tearoff=0)
        aboutMenu.add_command(label="About WormBait", command=self.showAboutWindow)
        menubar.add_cascade(label="About", menu=aboutMenu)
       
        self.entryList.grid(column=0, row=0, columnspan=2, sticky='NSEW')
        
        self.dbFileEntry = tkinter.Entry(self, textvariable=self.dbFilePath)
        self.dbFileEntry.grid(column=0, row=1, sticky='EW')

        dbFileBrowseButton = tkinter.Button(self, text="Browse...", command=self.OnDBBrowseButtonClick)
        dbFileBrowseButton.grid(column=1, row=1)
        
        self.outFileEntry = tkinter.Entry(self, textvariable=self.outFilePath)
        self.outFileEntry.grid(column=0, row=2, sticky='EW')

        outFileBrowseButton = tkinter.Button(self, text="Browse...", command=self.OnOutBrowseButtonClick)
        outFileBrowseButton.grid(column=1, row=2)

        self.button = ProcessButton(self)
        self.button.bind("<Return>", self.button.OnClick)
        self.button.grid(column=0,row=3)
        
        self.console = ConsoleBox(self, 30)
        self.console.grid(column=0,row=4, columnspan=2, sticky='NSEW')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.resizable(True,False)
        self.update()
        self.config(menu=menubar)     
        self.entryList.focus_set()

    def saveIniAndDestroy (self):
        config = SafeConfigParser()
        config.read('wormBait.ini')

        if not config.has_section('wormBait'):
            config.add_section('wormBait')

        xlocIDs = self.entryList.getValue()
        if '\n' in xlocIDs:
            xlocIDs = ','.join(xlocIDs.strip().split('\n'))
            
        config.set('wormBait', 'xlocIDs', xlocIDs)
        config.set('wormBait', 'degFile', self.dbFilePath.get())
        config.set('wormBait', 'outFile', self.outFilePath.get())

        with open('wormBait.ini', 'w') as f:
            config.write(f)

        self.destroy()

    def parseConfig (self):
        config = SafeConfigParser()
        config.read('wormBait.ini')

        configXlocs = ""
        configDegFile = ""
        configOutFile = ""
        
        if config.has_section('wormBait'):
            configXlocs = config.get('wormBait', 'xlocIDs')
            configDegFile = config.get('wormBait', 'degFile')
            configOutFile = config.get('wormBait', 'outFile')

        if configXlocs:
            self.entryList.writeln(configXlocs)
        else:
            self.entryList.writeln("Enter XLOC IDs here")

        if configDegFile:
            self.dbFilePath.set(configDegFile)
        else:
            self.dbFilePath.set('Enter path to DEG file here')

        if configOutFile:
            self.outFilePath.set(configOutFile)
        else:
            self.outFilePath.set('Enter desired path to output CSV file here')

    def OnDBBrowseButtonClick (self, *ignore):
        dialogReturn = tkinter.filedialog.askopenfilename(filetypes=[('Comma-separated value', '*.csv')])
        self.dbFilePath.set(dialogReturn)

    def OnOutBrowseButtonClick (self, *ignore):
        dialogReturn = tkinter.filedialog.asksaveasfilename(filetypes=[('Comma-separated value', '*.csv')])
        self.outFilePath.set(dialogReturn)

    def showAboutWindow (self):
        aboutWindow = AboutWindow(self)
        
        

if __name__ == "__main__":
    app = wormbaitWindow(None)
    app.title('WormBait')
    app.mainloop()
