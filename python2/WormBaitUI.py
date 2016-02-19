import Tkinter
from ScrolledText import ScrolledText
import WormCSV
import re
import threading

"""The WormBaitUI module holds the custom classes that make up the user interface layer in WormBait

These classes are the custom extensions of UI classes that are used in the WormBait UI. There
are a number of boilerplate classes that are also used in the UI.

Christopher Anna, 2/18/2016
"""
class ConsoleBox (ScrolledText):
    """The scrolling output text box that holds text in WormBait

    ConsoleBox extends ScrolledText and adds a couple convenience methods as well as
    keyboard shortcuts. Some methods are publicly exposed to make writing text
    more accessible to other components. This class is used both as the input and
    the output text in the final UI
    """
    
    def __init__(self, parent, height=25):
        """Constructs the ConsoleBox object.

        Most of the heavy lifting is done by the superconstructor, but
        we also perform the shortcut binding here.
        """
        
        ScrolledText.__init__(self, parent, width=80, height=height)
        self.bindShortcuts()
        self.parent = parent

    def bindShortcuts (self):
        """Creates shortcuts for Windows and OSX to highlight all text in the box"""
        self.bind("<Control-Key-a>", self.highlightAll)
        self.bind("<Control-Key-A>", self.highlightAll)
        self.bind("<Command-A>", self.highlightAll)
        self.bind("<Command-a>", self.highlightAll)

    def write (self, text):
        """Writes text to the ConsoleBox. Does not terminate with a newline"""
        self.insert(Tkinter.END, text)
        self.see(Tkinter.END)

    def writeln (self, text):
        """Writes text to the ConsoleBox. Terminates with a newline"""
        self.insert(Tkinter.END, text + '\n')
        self.see(Tkinter.END)

    def clear (self):
        """Wipes the text from the ConsoleBox"""
        self.delete('1.0', 'end')

    def getValue (self):
        """Gets all of the text in the ConsoleBox"""
        return self.get('1.0', 'end-1c')

    def highlightAll (self, *ignore):
        """Highlights all text in the ConsoleBox"""
        self.tag_add(Tkinter.SEL, "1.0", Tkinter.END)
        self.mark_set(Tkinter.INSERT, "1.0")
        self.see(Tkinter.INSERT)
        return 'break'

class ProcessButton (Tkinter.Button):
    """The ProcessButton is the component that kicks off the run of WormBait. Extends Tkinter.Button"""
    
    def __init__(self, parent):
        """Constructs a ProcessButton.

        No extra functionality is added here besides assigning some values to the superconstructor
        """
        
        Tkinter.Button.__init__(self, parent, text="Process", command=self.OnClick)
        self.parent = parent

    def OnClick (self, *ignore):
        """Kicks off a thread that performs the WormBait run"""
        
        t = threading.Thread(target=self.process)
        t.start()

    def log (self, text):
        """Convenience method to write text to the parent UI's ConsoleBox

        Writes text to the parent's console without a newline terminator
        """
        self.parent.console.write(text)

    def logln (self, text):
        """Convenience method to write text to the parent UI's ConsoleBox

        Writes text to the parent's console with a newline terminator
        """
        self.log(text + '\n')

    def collect_xloc_ids (self, rawText):
        """Collects and scrubs the XLOC IDs from the input console

        After some effort, the IDs can now be separated by any combination of
        newlines and commas. Whitespace is stripped from beginning and end
        """
        xlocIds = rawText.split('\n') # Split up rows
        xlocIds = [re.compile("[ ,]").split(i) for i in xlocIds] # Split apart rows by spaces
        xlocIds = [i for sublist in xlocIds for i in sublist] # Flatten sublists into one level
        cleanIds = [x.strip() for x in xlocIds] # Remove whitespace from each ID
        cleanIds = filter(None, cleanIds) # Remove all empty IDs
        return cleanIds
        
    def process (self):
        """Performs the 'run' of WormBait - collects all data from WormBase and writes it to the output file"""
        self.parent.console.clear()

        # First, some error handling. The input console needs some number of XLOC IDs
        # to perform a run
        listEntryText = self.parent.entryList.getValue()
        if not str(listEntryText) or str(listEntryText).startswith('Enter'):
            self.logln('Please enter some number of XLOC IDs')
            return

        # The CuffLink database file path must be specified
        dbFilePath = self.parent.dbFilePath.get()
        if not dbFilePath or dbFilePath.startswith('Enter'):
            self.logln('Please choose a path to the database file')
            return
        else:
            self.parent.console.writeln('Database file located at: ' + self.parent.dbFilePath.get())

        # The desired output file path must be specified
        outFilePath = self.parent.outFilePath.get()
        if not outFilePath or outFilePath.startswith('Enter'):
            self.logln('Please choose a path to the output file')
            return
        else:
            self.parent.console.writeln('Writing output CSV to: ' + outFilePath)

        self.logln('Processing...')
        cleanIds = self.collect_xloc_ids(listEntryText)

        # Build the object representing the CuffLink DB
        with open(self.parent.dbFilePath.get(), 'r') as csvDatabaseFile:
            self.csvDatabase = WormCSV.CuffLinkDatabase(csvDatabaseFile)

        # Initialize the list of WormData objects
        allWormDatas = []

        
        self.logln('Beginning data collection from WormBase (this could take a bit)')

        # This loop contains all of the WormBase API interactions
        for id in cleanIds:
            self.log(id + ' ... ')

            wormbaseIDs = self.csvDatabase.get(id)['gene'].split(',')

            for i in wormbaseIDs:
                # Create the WormData object. The object populates its own data in its constructor
                d = WormCSV.WormData(id, i, self.csvDatabase)
                d.data['xloc_id'] = id
                allWormDatas.append(d)
            
            self.logln('finished')

        self.logln('Finished collecting data from WormBase')

        # This list of headers can be subject to change in the future. For now,
        # it is fixed
        headers = ['xloc_id', 'gene_id', 'up/down', 'sequence_name', 'protein_id', 
                   'best_human_ortholog', 'description', 'gene_class', 'human_orthologs',
                   'nematode_orthologs', 'other_orthologs']

        self.log('Writing output CSV file ... ')
        output = WormCSV.OutputCSV(outFilePath, headers)
        output.write(allWormDatas)
        self.logln('finished!')
        self.log('Run complete!')

class AboutWindow (Tkinter.Toplevel):
    """The window with the 'About WormBait' information

    Just a small simple window that displays the boilerplate 'About' information like version number,
    licensing, and author contact info
    """
    
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
