#!/usr/bin/env python
import sys
import os
import hashlib
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFileDialog


#######################
###    FUNCTIONS    ###
#######################

logoLineA = ('  \____            ____ \n')
logoLineB = ('   \   \           \   \ \n')
logoLineC = ('    \SMC\_____      \   \ \n')
logoLineD = ('     \...~-__()______\___\_____________________ \n')
logoLineE = ("      \        Simon's Hash Info Finder Tool___\ \n")
logoLineF = ('       \     oo ooooooooooooooooooooo o o  |_O__\_ \n')
logoLineG = ('        ~~--_________/~~~/________________________) \n')
logoLineH = ('             |      /   /()                  | \n')
logoLineI = ('             0     /   /()                   0 \n')
logoLineJ = ('                  /___/                         \n\n')  
logoLineK = ('\t\tSHIFT Results Below\n\n')

def shiftLogo():
    print logoLineA, logoLineB, logoLineC, logoLineD, logoLineE, logoLineF, logoLineG, logoLineH, logoLineI, logoLineJ

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
        retval = hashlib.md5(open(filename, 'rb').read()).hexdigest()

#     print 'MD5 hash for: ' , filename , retval
     return retval
    
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
          retval = m.hexdigest()
        
     else:
         retval = hashlib.sha1(open(filename, 'rb').read()).hexdigest()

# print 'SHA1 hash for: ' , filename , retval
     return retval


########################
### END OF FUNCTIONS ###
########################

shiftLogo()

# Sets the size of Tkinter box
root = Tk()
root.geometry('255x150+300+100')
root.title("SHIFT, 2014")
# Text when opening program
text = Text(root)
text.insert(INSERT, "Please browse to hashfile...")
text.pack()



# Use hashfile in folder shift.py is sitting in
currentDir = os.getcwd()
hashFileName = os.path.normpath(currentDir + '\\shiftDir\hashfile')

# hashFileName = eg.enterbox(msg="Syntax: \<directory>\<directory>\<filename> example: C:\Users\Simon\Desktop\hashfile \n\n Please type in the location of the hashfile using above syntax: ", title="Shift - Sopia Suite")
# Text when opening program
text = Text(root)
text.insert(INSERT, "Please browse to folder you wish to scan...")
text.pack()

searchDirPath = tkFileDialog.askdirectory()
if searchDirPath == "":
    sys.exit(1)

# Opens the file containing hashes and checks for errors
try:
   hash_f = open(hashFileName, 'r')
except IOError:
    print 'cannot open file: ', hashFileName
    sys.exit(1)

if not os.path.isdir(searchDirPath):
    print 'cannot find search dir: ', searchDirPath
    sys.exit(1)


hashes = hash_f.read()

text_file = open('shiftDir\shiftOutput.txt', 'w')
text_file.write(logoLineA)
text_file.write(logoLineB)
text_file.write(logoLineC)
text_file.write(logoLineD)
text_file.write(logoLineE)
text_file.write(logoLineF)
text_file.write(logoLineG)
text_file.write(logoLineH)
text_file.write(logoLineI)
text_file.write(logoLineJ)
text_file.write(logoLineK)

numMD = 0
numSHA = 0

for dirname, dirnames, filenames in os.walk(searchDirPath):
    # print path to all filenames.
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        h_md5 = getFileHashMD5 (fullname)
		
        if h_md5 in hashes:
            numMD += 1
            #print num #global variable so we can use num outside of function/if statement
            text_file.write('\n\nMD5 Hash Match: ' + h_md5)
            text_file.write('\nFile Location : ' + os.path.normpath(fullname))
            print "\nMD5 match: ", h_md5, os.path.normpath(fullname),"\n"
        else:
            "\nNo known MD5 hashes were found.\n"


        h_sha1 = getFileHashSHA1 (fullname)
        if h_sha1 in hashes:
            numSHA += 1
            text_file.write('\n\nSHA1 Hash Match: ' + h_sha1)
            text_file.write('\nFile Location  : ' + os.path.normpath(fullname))
            print "SHA1 match  : ", h_sha1, os.path.normpath(fullname),"\n"
        else:
            "\nNo known SHA-1 hashes were found.\n" # Don't print or it loops 100's of times...


# Pop up GUI with results

tkMessageBox.showinfo("SHIFT, 2014", "\nFound " + str(numMD) + " MD5 match(es).\n\nFound " + str(numSHA) + " SHA-1 match(es).\n\nThank you for using Shift!\n\nPlease note: results have been created in the SHIFT directory\nfilename: " + text_file.name)

text_file.write('\n\n\nFound ' + str(numMD) + ' MD5 match(es)')
text_file.write('\nFound ' + str(numSHA) + ' SHA-1 match(es)')
text_file.write('\n\n\nIf space above is blank, Shift found 0 MD5 | SHA-1 matches.')
text_file.write('\n\n\n\t\tThank you for using shift!')
print "File results can be found in the shift directory, file: ", text_file.name

# This was causing problems! I had to close txt file before I could re-open it to read it!
text_file.close()

if tkMessageBox.askyesno("SHIFT, 2014", "Do you wish to view this file in the terminal now?"):
	with open ("shiftDir\shiftOutput.txt") as myTxt:
		print myTxt.read()
else:
	print "\nThank you for using SHIFT! Goodbye!\n"

#cleaning up
hash_f.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~ DEBUGGING SECTION - IGNORE EVERYTHING BELOW THIS LINE ~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Mac: /Users/simon/Desktop/
# Windows: C:\Users\Si\Desktop\
# Linux: /home/puzzle/Desktop

# C:\Users\Si\Desktop\sopiaSuite.gui\shift.SimonsHashInfoFinderTool\hashfile
# C:\Users\Si\Desktop\build
# print 'my os.getcwd =>', os.getcwd( ) # show my cwd execution dir
