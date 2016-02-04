import Tkinter
from ScrolledText import ScrolledText
import WormCSV
import re
import threading

class ConsoleBox (ScrolledText):
    def __init__(self, parent, height=25):
        ScrolledText.__init__(self, parent, width=80, height=height)
        self.bindShortcuts()
        self.parent = parent

    def bindShortcuts (self):
        self.bind("<Control-Key-a>", self.highlightAll)
        self.bind("<Control-Key-A>", self.highlightAll)
        self.bind("<Command-A>", self.highlightAll)
        self.bind("<Command-a>", self.highlightAll)

    def write (self, text):
        self.insert(Tkinter.END, text)
        self.see(Tkinter.END)

    def writeln (self, text):
        self.insert(Tkinter.END, text + '\n')
        self.see(Tkinter.END)

    def clear (self):
        self.delete('1.0', 'end')

    def getValue (self):
        return self.get('1.0', 'end-1c')

    def highlightAll (self, *ignore):
        self.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
        self.mark_set(Tkinter.INSERT, "1.0")
        self.see(Tkinter.INSERT)
        return 'break'

class ProcessButton (Tkinter.Button):
    def __init__(self, parent):
        Tkinter.Button.__init__(self, parent, text="Process", command=self.OnClick)
        self.parent = parent

    def OnClick (self, *ignore):
        t = threading.Thread(target=self.process)
        t.start()

    def log (self, text):
        self.parent.console.write(text)

    def logln (self, text):
        self.log(text + '\n')

    def collect_xloc_ids (self, rawText):
        xlocIds = rawText.split('\n') # Split up rows
        xlocIds = [re.compile("[ ,]").split(i) for i in xlocIds] # Split apart rows by spaces
        xlocIds = [i for sublist in xlocIds for i in sublist] # Flatten sublists into one level
        cleanIds = [x.strip() for x in xlocIds] # Remove whitespace from each ID
        cleanIds = filter(None, cleanIds) # Remove all empty IDs
        return cleanIds
        
    def process (self):
        self.parent.console.clear()
        
        listEntryText = self.parent.entryList.getValue()
        if not str(listEntryText) or str(listEntryText).startswith('Enter'):
            self.logln('Please enter some number of XLOC IDs')
            return

        dbFilePath = self.parent.dbFilePath.get()
        if not dbFilePath or dbFilePath.startswith('Enter'):
            self.logln('Please choose a path to the database file')
            return
        else:
            self.parent.console.writeln('Database file located at: ' + self.parent.dbFilePath.get())

        outFilePath = self.parent.outFilePath.get()
        if not outFilePath or outFilePath.startswith('Enter'):
            self.logln('Please choose a path to the output file')
            return
        else:
            self.parent.console.writeln('Writing output CSV to: ' + outFilePath)

        self.logln('Processing...')
        cleanIds = self.collect_xloc_ids(listEntryText)

        with open(self.parent.dbFilePath.get(), 'r') as csvDatabaseFile:
            self.csvDatabase = WormCSV.CuffLinkDatabase(csvDatabaseFile)

        allWormDatas = []
        self.logln('Beginning data collection from WormBase (this could take a bit)')
        for id in cleanIds:
            self.log(id + ' ... ')

            wormbaseIDs = self.csvDatabase.get(id)['gene'].split(',')

            for i in wormbaseIDs:
                d = WormCSV.WormData(id, i, self.csvDatabase)
                d.data['xloc_id'] = id
                allWormDatas.append(d)
            
            self.logln('finished')

        self.logln('Finished collecting data from WormBase')

        headers = ['xloc_id', 'gene_id', 'up/down', 'sequence_name', 'protein_id', 
                   'best_human_ortholog', 'description', 'gene_class', 'human_orthologs',
                   'nematode_orthologs', 'other_orthologs']

        self.log('Writing output CSV file ... ')
        output = WormCSV.OutputCSV(outFilePath, headers)
        output.write(allWormDatas)
        self.logln('finished!')
        self.log('Run complete!')

class AboutWindow (Tkinter.Toplevel):
    def __init__ (self, parent):
        Tkinter.Toplevel.__init__(self, parent)
        self.parent = parent
        self.buildContent()

    def buildContent (self):
        self.title("About WormBait")
        self.grid()

        img = Tkinter.PhotoImage(file="../img/worm.gif")
        imgPanel = Tkinter.Label(self, image=img)
        imgPanel.image = img;
        imgPanel.grid(row = 0, column = 0, rowspan = 2)

        versionLabel = Tkinter.Label(self, text="WormBait v" + self.parent.VERSION, font=("Helvetica", 16))
        versionLabel.grid(row = 0, column = 1)

        copyright = "WormBait is free to use and distribute.\nChristopher Anna 2016\ncanna12@gmail.com"
        copyrightLabel = Tkinter.Label(self, text=copyright)
        copyrightLabel.grid(row = 1, column = 1)

        closeButton = Tkinter.Button(self, text="Close", command = self.destroy)
        closeButton.grid(row = 2, column = 1, columnspan = 2)    
