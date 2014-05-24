import os, sys, platform # Platform to detect OS running script
from os import stat
from datetime import datetime
from time import gmtime, strftime
import shutil
import time
import hashlib
# Importing tkinter GUI
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFileDialog

#from pwd import getpwuid # works on mac but not windows (offically)

#######################
###    FUNCTIONS    ###
#######################

# Fibs Skull logo printed to shell
aa =("          _,.-------.,_        ")
bb =("      ,;~'             '~;,    ")
cc =("    ,;                     ;,   ")
dd =("   ;     Welcome to FIBS     ;  ")
ee =("  ,'   (file investigation    ',")
ff =(" ,;         bite-size)         ;")
gg =(" ; ;      .           .      ; ;")
hh =(" | ;   ______       ______   ; |") 
ii =(" |  `/~'     ~' . '~     '~\'  |")
jj =(" |  ~  ,-~~~^~, | ,~^~~~-,  ~  |")
kk =("  |   | SIMONS}:{  SUITE |   | ") 
ll =("  |   l SOPIA / | \  2014!   | ")
mm =("  .~  (__,.--' .^. '--.,__)  ~. ")
nn =("  |     ---;' / | \ `;---     | ") 
oo =("   \__.       \/^\/       .__/  ")
pp =("    V| \                 / |V   ")
qq =("     | |T~\___!___!___/~T| |    ")
rr =("     | |`IIII_I_I_I_IIII'| |    ")
ss =("     |  \,III I I I III,/  |    ")
tt =("     \    `~~~~~~~~~~'    /     ")
uu =("        \   .       .   /       ")
vv =("          \.    ^    ./         ") 
ww =("            ^~~~^~~~^           ")

def hideWindow():
		root.withdraw()

def printLogo():
	print aa
	print bb
	print cc
	print dd
	print ee
	print ff
	print gg
	print hh
	print ii
	print jj
	print kk
	print ll
	print mm
	print nn
	print oo
	print pp
	print qq
	print rr
	print ss
	print tt
	print uu
	print vv
	print ww

# Sets the size of Tkinter box
root = Tk()
root.geometry('255x150+300+100')
root.title("SPIES, 2014")

def askDirToScan():
	root = Tk()
	root.withdraw()
	global searchAbsolutePath
	searchAbsolutePath = tkFileDialog.askdirectory()
	# , "Browse to the directory you wish to search")
	if searchAbsolutePath == "": 
		tkMessageBox.showinfo("FIBS, 2014", "\n\nThank you for using Fibs! Goodbye!\n")
		sys.exit(0)


FILESIZE_SLICING_LIMIT = 5000000 #bytes - 4.76837mb




def getFileHashMD5(filename):
     retval = 0;
     filesize = os.path.getsize(filename)
    
     if filesize > FILESIZE_SLICING_LIMIT:
        with open(filename, 'rb') as fh:
          m = hashlib.md5()
          while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
          retval = m.hexdigest()
        
     else:
     	global md5Val
        md5Val = hashlib.md5(open(filename, 'rb').read()).hexdigest()

def getFileHashSHA1(filename):
     retval = 0;
     filesize = os.path.getsize(filename)
    
     if filesize > FILESIZE_SLICING_LIMIT:
        with open(filename, 'rb') as fh:
          m = hashlib.sha1()
          while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
          shaVal = m.hexdigest()
        
     else:
     	 global shaVal
         shaVal = hashlib.sha1(open(filename, 'rb').read()).hexdigest()



########################
### END OF FUNCTIONS ###
########################

printLogo()
hideWindow()

num = 1000
#Detect OS
print "Detecting OS..."
osType = platform.system()
print "OS Detected: " + osType

# Ask user if they want to capture live processes of machine (Linux & Mac only)
fileExts = [('html','*.html')]
if osType == 'Windows':
    pass
elif osType == 'Darwin' or 'Linux':
	if tkMessageBox.askyesno("FIBS, 2014", "Do you want to capture live processes of this machine?"):
		processOutput = (os.popen("ps -Af").read())
		capProcessesTime = datetime.now() # Assign current timestamp to a variable to be used later
		#Prompt user where to save results in .txt format ONLY
		processesHTMLLocation = tkFileDialog.asksaveasfilename(parent=root,filetypes=fileExts ,title="Save the file as...")
		with open(processesHTMLLocation,'w') as f:
			        f.write('Below is a list of processes captured live at the following date + time: '+ str(capProcessesTime) + "\n\n")
			        f.write(processOutput)
			        f.write('\n\n\nThank you for using Fibs!\nFibs is part of Sopia Suite, 2014.')
			        f.close()
			        if tkMessageBox.askyesno("FIBS, 2014", "Do you wish to continue using FIBS?"):
			            pass
			        else:
			            tkMessageBox.showinfo("FIBS, 2014", "\n\nThank you for using Fibs! Goodbye!\n")
			            sys.exit(0)
	elif tkMessageBox.askyesno("FIBS, 2014", "Do you wish to continue using FIBS?"):
		pass
	else:
		tkMessageBox.showinfo("FIBS, 2014", "\n\nThank you for using Fibs! Goodbye!\n")
		sys.exit(0)


# tkMessageBox.showinfo("FIBS, 2014", "Browse to the directory you wish to search e.g C:\Users\Simon\Desktop")
# searchAbsolutePath = tkFileDialog.askdirectory()

askDirToScan()

print "\n\nFolder Selected: " + os.path.normpath(searchAbsolutePath)
hideWindow()


saveFileLocation = os.getcwd()
print saveFileLocation

# The following just ensures the output is stored in correct place
if osType == 'Windows':
	resultsHTMLLocation = saveFileLocation + '\\fibsDir\output.html'
elif osType == 'Darwin' or 'Linux':
	resultsHTMLLocation = saveFileLocation + '/fibsDir/output.html'

start = datetime.now()

# Create html file in location user input into the previous window
with open(resultsHTMLLocation,'w') as f:
    f.write('<html> \n\n')
    f.write('\n<img src="./logo/fibsLogo.png" alt="logo"> <br>')
    f.write('\n\n\nYou searched the following directory: \n' + os.path.normpath(searchAbsolutePath) + '\n\n\n')
    f.write('<br><br>Results for custom search: \n\n\n')
    for root, dirs, files in os.walk(searchAbsolutePath):
        for file in files:
            pathName = os.path.join(root,file)
            getFileHashMD5(pathName)
            getFileHashSHA1(pathName)
            #print pathName
            #print os.path.getsize(pathName)
            #print stat(searchAbsolutePath).st_uid
            #print getpwuid(stat(searchAbsolutePath).st_uid).pw_name # Only works on Mac

            f.write('<p>')
            f.write('<br>Fibs File Identifier: %d' % (num))
            f.write('<br>\n%d File Name: ' % num + file)
            #f.write('\nFile Owner: {}'.format(getpwuid(stat(searchAbsolutePath).st_uid).pw_name)) #Only works on Mac
            # IMPORTANT !!!! Was getting error on Linux CentOS (python v2.6, should work fine on Python v2.7.3) regarding 
            # "zero length field name in format". Added 0 in between line 201,202,203 {}
            f.write('<br>\n%d UID: {0} \n'.format(stat(searchAbsolutePath).st_uid)% num)
            f.write('<br>%d Enclosing Directory: {0}\n'.format(os.path.normpath(pathName))% num)
            f.write('<br>%d Size in Bytes: {0}\n\n'.format(os.path.getsize(pathName))% num)
            f.write('<br>%d File Hash (MD5): {0}'.format(md5Val)% num)
            f.write('<br>%d File Hash (SHA1): {0}'.format(shaVal)% num)
            f.write('</p>')
            num += 1 # Increments unique file ID. += means add right operand onto left operand. Increment +1
    
    f.write('\n\n</html>')
    f.close() #Close file

# finishWrite = datetime.now()
finishWrite = datetime.now()

difference = finishWrite - start
print "Difference is: " + str(difference)
formattedDifference = str(difference)
tkMessageBox.showinfo("FIBS, 2014", "\t\tFinished Processing Data" + "\n\n\tStarted processing data at: " +str(start) + "\n\nFind results at: " + "\n\n" + str(resultsHTMLLocation) + "\n\n\n\tTime taken to scan directory: (H,M,S,MS) " + str(formattedDifference))

# 'a' is to append
with open(resultsHTMLLocation,'a') as f:
    f.write("FiBs Stats: ") 
    f.write("Started processing data at: " +str(start))
    f.write("<br>Finished processing data at: " +str(finishWrite))
    f.write("<br>Total time taken to scan directory: (H,M,S,MS) " +(formattedDifference))
    f.write("<br><br>Thank you for using Fibs!")
    f.close()
print "\n\nResults saved at following location: " + resultsHTMLLocation
print "\n\nThank you for using FIBS"
tkMessageBox.showinfo("FIBS, 2014", "Thank you for using FIBS, Goodbye!")