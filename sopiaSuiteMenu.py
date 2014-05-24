from Tkinter import *
import Tkinter
import subprocess
import os
import sys

root = Tkinter.Tk()
root.title("SopiaSuite, 2014")
root.geometry('255x255+550+220')
text = Text(root)
text.insert(INSERT, "Please select which tool\nyou wish to use...")

def kill_window():
	root.destroy()

def callDuff():
    proc = subprocess.Popen("python duffDir\duff.py")
    kill_window()
    proc.wait()

def callFibs():
	proc = subprocess.Popen("python fibsDir\\fibs.py")
	kill_window()
	proc.wait()

def callShift():
	proc = subprocess.Popen("python shiftDir\shift.py")
	kill_window()
	proc.wait()

def callSpies():
	proc = subprocess.Popen("python spiesDir\spies.py")
	kill_window()
	proc.wait()

def callSiphon():
	print ("\nSIPHON is only compatible with Linux (Ubuntu)\nPlease run manually on Ubuntu.\n")

def callTrap():
	proc = subprocess.Popen("python trapDir\\trap.py")
	kill_window()
	proc.wait()

def callHelp():
	print "\nLaunching help files..."
	os.chdir("helpFiles")
	print os.getcwd()
	proc = subprocess.Popen("hh.exe sopiaChm.chm")
	os.getcwd()
	os.chdir("../")
	os.getcwd()

def callExit():
	print ("\nThank you for using SOPIA Suite\n\tGoodbye!\n")
	sys.exit(0)

buttonOne = Tkinter.Button(root, text ="DUFF", relief=FLAT, command=callDuff)
buttonTwo = Tkinter.Button(root, text ="FIBS", relief=FLAT, command=callFibs)
buttonThree = Tkinter.Button(root, text ="SHIFT", relief=FLAT, command=callShift)
buttonFour = Tkinter.Button(root, text ="SPIES", relief=FLAT, command=callSpies)
buttonFive = Tkinter.Button(root, text ="SIPHON", relief=FLAT, command=callSiphon)
buttonSix = Tkinter.Button(root, text ="HELP FILES", relief=FLAT, command=callHelp)
buttonSeven = Tkinter.Button(root, text ="EXIT", relief=FLAT, command=callExit)

buttonOne.pack()
buttonTwo.pack()
buttonThree.pack()
buttonFour.pack()
buttonFive.pack()
buttonSix.pack()
buttonSeven.pack()
text.pack()
root.mainloop()