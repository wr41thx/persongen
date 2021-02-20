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


from tkinter import *
import csv
import sys
import random

""" BuildGUI creates the GUI and defines functions for buttons"""
def BuildGUI():

    """Restart Button"""
    def restartGUI():
        root.destroy()
        BuildGUI()

    """Submit Button"""
    def subClick():

        """"Set up array for streets and error label"""
        streets = []
        errorLabel = Label(root, text="Error: Please enter a number to generate!")
        selectedStreet = StringVar()

        """Error Message if no entry"""
        if len(numGenEntry.get()) == 0:
            errorLabel.pack()
            return

        """Show a text response confirming entry after submission"""
        responseLabel = Label(root, text="You requested " + str(numGenEntry.get()) + " addresses for the state: " +
                                         selectedState.get())
        responseLabel.pack()

        """Follow same steps as command-line option, but with GUI data"""
        guiPath = "state_data/" + selectedState.get().lower() + ".csv"

        if selectedState.get().lower() == "mt":
            with open(guiPath, 'r') as csv_file:
                csv_reader = list(csv.reader(csv_file, delimiter=','))
        else:
            with open(guiPath, 'r', encoding='cp850') as csv_file:
                csv_reader = list(csv.reader(csv_file, delimiter=','))
        print("opening " + guiPath)

        """Get number of lines in appropriate csv file"""
        numLines = len(list(csv_reader))

        """Initialize counter to fill streets list"""
        fillCount = 0

        """ Fill streets list with appropriate number of pseudo-randomly selected street data"""
        while fillCount < int(numGenEntry.get()):
            randIndex = random.randrange(1, numLines - 50)
            randStreet = csv_reader[randIndex]

            """I tried refactoring the following, but it actually appears to catch more blank entries this way"""
            """This is a simple attempt to ignore entries with blank street names.  Why just street names?"""
            """New Mexico has no zip codes, and lots of these addresses have no house number."""
            if randStreet[1] == "" or randStreet[1] is None or randStreet[1] == " " or randStreet[1] == "N/A":
                randIndex = random.randrange(1, numLines - 50)
                randStreet = csv_reader[randIndex]
            else:
                formatStreet = randStreet[0] + " " + randStreet[1] + " " + randStreet[2] + " " + randStreet[3]
                streets.append(formatStreet)
                fillCount += 1

        csv_file.close()

        """Label to explain drop down"""
        cvsLabel = Label(root, text="Click the drop down below to preview addresses")
        cvsLabel.pack()

        '''Create a drop down full of addresses as a preview and pack'''
        streetDrop = OptionMenu(root, selectedStreet, *streets)
        selectedStreet.set(streets[0])
        streetDrop.pack()

        """Clean up interface to only show relevant information"""
        submitButton.destroy()
        buttonLabel.destroy()
        numGenLabel.destroy()
        stateDrop.destroy()
        stateLabel.destroy()
        myLabel2.destroy()

        """Outputs streets to output.csv"""
        def outputCSV():
            print("Writing output.csv...")
            with open('output.csv', 'w+', newline='') as output_file:
                csv_writer = csv.writer(output_file, delimiter=",")
                csv_writer.writerow(['State'] + ['Number to Generate'] + ['Type'] + ['Value'])

                for entry in streets:
                    csv_writer.writerow([selectedState.get()] + [int(numGenEntry.get())] + ["Street Address"] + [entry])

            output_file.close()
            numGenEntry.destroy()
            outputLabel = Label(root, text="\nOutput complete, please check program directory!\n")
            outputLabel.pack()
            print("output.csv is now in same directory as program!")

        """Create output CSV Button"""
        csvButton = Button(root, text="Output to CSV", command=outputCSV, fg="white", bg="green")
        csvButton.pack()

        '''Create and pack a simple restart button'''
        restartButton = Button(root, text="Restart", command=restartGUI, fg="white", bg="red")
        restartButton.pack()

    """This is where the initial GUI creation starts"""
    root = Tk()
    root.title("Person Generator by Theodor Melsheimer")
    root.geometry("640x480")

    """Creating a Label Widget"""
    myLabel1 = Label(root, text="PERSON GENERATOR")
    myLabel2 = Label(root, text="Please Enter a State and a Number of Addresses to Generate\n")

    """Put on screen"""
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

    """Drop Down Box"""
    stateLabel = Label(root, text="Select State")
    stateLabel.pack()
    stateDrop = OptionMenu(root, selectedState, *stateOptions)
    stateDrop.pack()

    """Number to generate input field"""
    numGenLabel = Label(root, text="\nNumber of Addresses to Generate")
    numGenLabel.pack()

    numGenEntry = Entry(root, width=10)
    numGenEntry.pack()

    """Submit Button"""
    buttonLabel = Label(root, text="\n\n\n\n\n\nClick here after selection!")
    buttonLabel.pack()
    submitButton = Button(root, text="Submit", command=subClick, fg="white", bg="green")
    submitButton.pack()

    """Run GUI loop"""
    root.mainloop()


"""*****************************************************************************************************************"""
"""***********************COMMAND LINE OPTION STARTS HERE***********************************************************"""
"""*****************************************************************************************************************"""

"""Initialize variables for path building, street list, and randomization"""
argCount = 0
csvExtension = ".csv"
stateDir = "state_data/"
streets = []
random.seed()
state = ""
genNum = 0
filename = ""
fullPath = ""
errorCheck = 0

"""Dictionary for interpreting full state name vs abbreviation"""
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

"""Check for arguments when run in command prompt"""
for arg in sys.argv:
    argCount += 1
if 1 < argCount < 3:

    print("Reading input.csv...")

    """Read the input.csv"""
    with open(sys.argv[1], 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        """Skip the Header"""
        next(csv_reader)
        """Get the state and number to generate from each line"""
        for line in csv_reader:
            state = line[0].lower()
            genNum = line[1]
        if state in stateKeys:
            state = stateDict[state]

    """Close input file and create path to appropriate csv file in state_data"""
    csv_file.close()
    fileName = state + csvExtension
    fullPath = stateDir + fileName

    print("Reading " + fileName + "...")

    """Open appropriate state csv file, new mexico has weird encoding problem and montana is only file that won't 
    accept the encoding required by new mexico....so this is my solution"""
    if state == "mt":
        with open(fullPath, 'r') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=','))
    else:
        with open(fullPath, 'r', encoding='cp850') as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=','))

    """Get number of lines in appropriate csv file"""
    numLines = len(list(csv_reader))

    print("Finding random addresses from " + str(numLines) + " entries...")
    fillCount = 0

    """ Fill streets list with appropriate number of pseudo-randomly selected street data"""
    while fillCount < int(genNum):
        randIndex = random.randrange(1, numLines - 50)
        randStreet = csv_reader[randIndex]
        """My attempt to clean some of this data up.  To be frank, these csv files are a huge mess :( """
        if randStreet[1] == "" or randStreet[1] is None or randStreet[1] == " " or randStreet[1] == "N/A":
            randIndex = random.randrange(1, numLines - 50)
            randStreet = csv_reader[randIndex]
        else:
            formatStreet = randStreet[0] + " " + randStreet[1] + " " + randStreet[2] + " " + randStreet[3]
            streets.append(formatStreet)
            fillCount += 1

        csv_file.close()
    print("Writing output.csv...")
    with open('output.csv', 'w+', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter=",")
        csv_writer.writerow(['State'] + ['Number to Generate'] + ['Type'] + ['Value'])

        for entry in streets:
            csv_writer.writerow([state] + [genNum] + ["Street Address"] + [entry])

    output_file.close()
    print("output.csv is now in same directory as program!")
    exit(0)

if argCount >= 3:
    print("Error: Can only accept single csv file as input!")
    exit(0)

else:
    """Start GUI if no arguments are passed"""
    BuildGUI()
