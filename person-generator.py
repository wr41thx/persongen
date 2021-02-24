# PERSON GENERATOR DRAFT BUILD
# Author: Theodor Melsheimer
# Date: 2/9/2021
# Class: CS 361 400 Winter 2021

# Description:
# This program generates a pseduo-randomly selected list of addresses
# based on the desired state and the number of addresses to generate.
# State addresses are supplied by files in state_data, which must be located
# in the same directory as the person-generator.py file.

# If run form the command line with no argument, it launches a graphical user interface.

# UPDATE 2/21/2021
# The program now shares information with life-generator.py.  These files are found in the life_gen folder.
# A *LOT* of refactoring going on here.  GenerateToys(), GenerateToyPreview(), CleanUp(), CreateResponseLabel(),
# CreateGUIPath(), CreateOutputLabel(), CreateCSVButton(), CreateRestartButton(),
# and more new functions to remove code smells and improve overall readability.
#

from tkinter import *
import csv
import sys
import random
import subprocess
import os.path

"""Initialize variables for path building, street list, and randomization"""
random.seed()
argCount = 0
toys = []
numStreets = 0
numToys = 0
csvExtension = ".csv"
stateDir = "state_data/"
streets = []
state = ""
toyCategory = ""
filename = ""
fullPath = ""
stateDict = {
    "alaska": "ak",
    "arizona": "az",
    "california": "ca",
    "colorado": "co",
    "hawaii": "hi",
    "idaho": "id",
    "montana": "mt",
    "new mexico": "nm",
    "nevada": "nv",
    "oregon": "or",
    'utah': "ut",
    "washington": "wa",
    "wyoming": "wy"
}

stateKeys = stateDict.keys()

"""Creates the output.csv File"""

def OutputCSV(state):
    print("Writing output.csv for person-generator")
    with open('output.csv', 'w+', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter=",")
        csv_writer.writerow(['State'] + ['Number to Generate'] + ['Type'] + ['Value'])

        for entry in streets:
            csv_writer.writerow([state] + [len(streets)] + ["Street Address"] + [entry])
        for entry in toys:
            csv_writer.writerow(entry)

    output_file.close()
    print("output.csv is now in same directory as program!")

"""Creates file path for appropriate state csv file"""

def CreatePath(state):
    path = "state_data/" + state + ".csv"
    return path

"""Appends output of life-generator to output of person-generator"""

def AppendToys():
    with open("output.csv", 'a+', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',')
        for line in toys:
            csv_writer.writerow(line)

"""Fills streets array with filtered street addresses"""

def FillStreets(csv_reader, numStreets):
    numLines = len(list(csv_reader))
    fillCount = 0
    while fillCount < numStreets:
        randIndex = random.randrange(1, numLines - 50)
        randStreet = csv_reader[randIndex]
        if randStreet[1] == "" or randStreet[1] is None or randStreet[1] == " " or randStreet[1] == "N/A":
            randIndex = random.randrange(1, numLines - 50)
            randStreet = csv_reader[randIndex]
        else:
            formatStreet = randStreet[0] + " " + randStreet[1] + " " + randStreet[2] + " " + randStreet[3]
            streets.append(formatStreet)
            fillCount += 1

"""Creates a toys.csv file for life-generator.py input"""

def CreateToysCSV(numToys, toyCategory):
    with open("toys.csv", "w", newline='') as output_file:
        print("Creating toys.csv for life-generator")
        csv_writer = csv.writer(output_file, delimiter=",")
        csv_writer.writerow(['input_item_type'] + ['input_item_category'] + ['input_number_to_generate'])
        csv_writer.writerow(['toys'] + [toyCategory] + [numToys])
    output_file.close()

"""Runs life-generator.py subprocess and generates a list of toys from life_gen output.csv"""

def GenerateToys():
    print("toy.csv found!")
    print("Running life-generator.py with toys.csv")
    subprocess.call(["python", "./life_gen/life-generator.py", "toys.csv"])
    print("File output.csv written to ./life_gen!")
    print("Appending life-gen output to person-gen output!")
    with open("./life_gen/output.csv", 'r') as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        for line in csv_reader:
            toys.append(line)
    csv_file.close()

"""Returns appropriate state csv file"""

def GetStateCSV(state, guiPath):
    if state == "mt":
        with open(guiPath, 'r') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=','))
    else:
        with open(guiPath, 'r', encoding='cp850') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=','))
    print("opening " + guiPath)
    csv_file.close()
    return csv_reader

"""Creates GUI and defines GUI related functions"""

def BuildGUI():
    def RestartGUI():
        toys.clear()
        streets.clear()
        root.destroy()
        BuildGUI()

    def CreateCSVButton():
        csvButton = Button(root, text="Output to CSV", command=OutputCSVBtn, fg="white", bg="green")
        csvButton.pack()

    def CreateRestartButton():
        restartButton = Button(root, text="Restart", command=RestartGUI, fg="white", bg="red")
        restartButton.pack()

    def CreateOutputLabel():
        outputLabel = Label(root, text="\nOutput complete, please check program directory!\n")
        outputLabel.pack()

    """Outputs streets and toys to output.csv (Button Function)"""

    def OutputCSVBtn():
        OutputCSV(selectedState.get().lower())
        CreateOutputLabel()

    """Creates a preview list with just the toy names"""

    def GenerateToyPreview():
        toyPreview = []
        isFirst = True
        for line in toys:
            if isFirst is True:
                isFirst = False;
            else:
                toyPreview.append(line[3])
        return toyPreview

    """Clean up interface after submission"""

    def CleanUp():
        submitButton.destroy()
        buttonLabel.destroy()
        numGenLabel.destroy()
        toyNumGenLabel.destroy()
        toyDrop.destroy()
        stateDrop.destroy()
        stateLabel.destroy()
        toyLabel.destroy()
        myLabel2.destroy()
        numGenEntry.destroy()
        toyNumGenEntry.destroy()

    def CreateResponseLabel():
        responseLabelStreets = Label(root, text="You requested " + numGenEntry.get() + " addresses for the state: " +
                                                selectedState.get() + "\n")
        responseLabelStreets.pack()
        responseLabelToys = Label(root, text="You requested " + toyNumGenEntry.get() + " Toys for the category: " +
                                             selectedToy.get() + "\n")
        responseLabelToys.pack()

    def CreatePreview(selectedStreet, toyPreview):
        """Label for streets drop down"""
        cvsLabel = Label(root, text="Click the drop down below to preview addresses")
        cvsLabel.pack()

        """Create a drop down full of addresses as a preview and pack"""
        streetDrop = OptionMenu(root, selectedStreet, *streets)
        selectedStreet.set(streets[0])
        streetDrop.pack()

        """Label for toy drop down"""
        toyPreviewLabel = Label(root, text="\nClick the drop down to preview toys")
        toyPreviewLabel.pack()

        """Toy drop down"""
        toyPrevDrop = OptionMenu(root, selectedToy, *toyPreview)
        selectedToy.set(toyPreview[0])
        toyPrevDrop.pack()

    """Submit Button, sends all data for processing, generates results screen"""

    def subClick():
        if len(numGenEntry.get()) == 0 or len(toyNumGenEntry.get()) == 0:
            return
        selectedStreet = StringVar()
        numStreets = int(numGenEntry.get())
        numToys = int(toyNumGenEntry.get())
        state = selectedState.get().lower()
        toyCategory = selectedToy.get()
        CreateResponseLabel()
        guiPath = CreatePath(state)
        csv_reader = GetStateCSV(state, guiPath)
        FillStreets(csv_reader, numStreets)
        CreateToysCSV(numToys, toyCategory)
        GenerateToys()
        toyPreview = GenerateToyPreview()
        CreatePreview(selectedStreet, toyPreview)
        CreateCSVButton()
        CreateRestartButton()
        CleanUp()

    """Create Root and Starting Prompts / Labels"""
    root = Tk()
    root.title("Person Generator by Theodor Melsheimer")
    root.geometry("640x480")

    """Title"""
    myLabel1 = Label(root, text="PERSON GENERATOR")
    myLabel2 = Label(root, text="Please Enter a State and a Number of Addresses to Generate\n")
    myLabel1.pack()
    myLabel2.pack()

    """State Selections for drop down"""
    stateOptions = [
        "AK",
        "AZ",
        "CA",
        "CO",
        "HI",
        "ID",
        "MT",
        "NM",
        "NV",
        "OR",
        "UT",
        "WA",
        "WY"
    ]
    selectedState = StringVar()
    selectedState.set(stateOptions[0])

    """Toy Selections for drop down"""
    toyOptions = [
        "Arts & Crafts",
        "Baby & Toddler Toys",
        "Characters & Brands",
        "Die-Cast & Toy Vehicles",
        "Educational Toys",
        "Electronic Toys",
        "Figures & Playsets",
        "Games",
        "Jigsaws & Puzzles",
        "Musical Toy Instruments",
        "Novelty & Special Use",
        "Pretend Play",
        "Sports Toys & Outdoor"
    ]
    selectedToy = StringVar()
    selectedToy.set(toyOptions[0])

    """Drop Down Box"""
    stateLabel = Label(root, text="Select State")
    stateLabel.pack()
    stateDrop = OptionMenu(root, selectedState, *stateOptions)
    stateDrop.pack()

    """Number to generate input field for streets"""
    numGenLabel = Label(root, text="\nNumber of Addresses to Generate")
    numGenLabel.pack()
    numGenEntry = Entry(root, width=10)
    numGenEntry.pack()

    """Drop Down Box for Toy Selection"""
    toyLabel = Label(root, text="\nSelect a Toy Category")
    toyLabel.pack()
    toyDrop = OptionMenu(root, selectedToy, *toyOptions)
    toyDrop.pack()

    """Number to generate input field for toys"""
    toyNumGenLabel = Label(root, text="\nNumber of Toys to Generate")
    toyNumGenLabel.pack()
    toyNumGenEntry = Entry(root, width=10)
    toyNumGenEntry.pack()

    """Submit Button"""
    buttonLabel = Label(root, text="\n\n\n\n\n\nClick here after selection!")
    buttonLabel.pack()
    submitButton = Button(root, text="Submit", command=subClick, fg="white", bg="green")
    submitButton.pack()

    """Run GUI loop"""
    root.mainloop()


"""*****************************************************************************************************************"""
"""***********************************COMMAND LINE OPTION STARTS HERE***********************************************"""
"""*****************************************************************************************************************"""

"""Check for arguments when run in command prompt"""
for arg in sys.argv:
    argCount += 1
if 1 < argCount < 3:
    print("Reading input.csv...")

    """Read the input.csv for state and number to generate"""
    with open(sys.argv[1], 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            state = line[0].lower()
            numStreets = int(line[1])
        if state in stateKeys:
            state = stateDict[state]
    csv_file.close()

    """Open state.csv, process, output.csv"""
    fullPath = CreatePath(state)
    print("Reading " + fullPath + "...")
    csv_reader = GetStateCSV(state, fullPath)
    FillStreets(csv_reader, numStreets)
    OutputCSV(state)

    """Check for valid life-generator.py input, process, append to output.csv"""
    print("Searching for toys.csv...")
    if os.path.exists('toys.csv'):
        GenerateToys()
        AppendToys()
    else:
        print('toys.csv not found, closing person-generator.py!')
    exit(0)

if argCount >= 3:
    print("Error: Can only accept single csv file as input!")
    exit(0)

else:
    BuildGUI()
