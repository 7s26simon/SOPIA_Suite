import subprocess, csv, stat, shutil, time
import os, sys, platform # Detect OS
# Importing tkinter GUI
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFileDialog

def closeWindow():
  root.withdraw()

# Logo

siphonLogo = '''

                               [===============-o___
                               ||              (____)
                               ||              |    |
                            ~  ||              | o  |
                            __ ||              |    |
                            || ||              |    |
                          .-||-||-.            |   o| 
                         _\_______/_===========|o   |
                          )\_____/(            |~~~~|
                         /     ||  \           |    |
                        /      ||   \          | ~  |
                       /       ||    \         |  ~ |
                      /~~~~~~~~~~~~~~~\        |~   |
                     /  SIPHON ::      \       |  ~ |
                    (    SOPIA :: SUITE )      |~   |
                     `-----------------'       |____|

                     '''

# Sets the size of Tkinter box
root = Tk()
root.geometry('255x150+300+100')
root.title("SIPHON, 2014")
# Text when opening program
text = Text(root)
text.insert(INSERT, "Please browse to libesedb-20120102 folder...")
text.pack()


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)



closeWindow()
print siphonLogo
osType = platform.system()
print ("You are using: " + osType + ("\n\nNote: SIPHON is only supported on Ubuntu.\nFor further Information, please consult\nthe help files that came with SopiaSuite."))
if osType == ('Linux'):
    pass
elif osType == ('Windows') or ('Darwin'):
  print ("Sorry, SIPHON is only compatible with Linux. For more details, please see\nthe help files.")
  sys.exit(1)

print ("\n")
thumbcacheID = raw_input("Please enter thumbcacheID you\nwish to search the database for: ")
# b014618486f9299e

print ("\nPlease browse to libesedb-20120102/esedbtools directory")

cwd = os.getcwd()

esedbToolsLocation = (cwd + '/libesedb-20120102/esedbtools')

print ("\nPlease browse to Windows.edb file")

windowsEdbLocation = (cwd + '/evidence/Windows.edb')

print esedbToolsLocation  + "     ESE TOOLS LOCATION\n"
print windowsEdbLocation  + "     WINDOWS EDB FILE LOCATION"

# enter libesedb directory:
with cd(esedbToolsLocation):
   print ("\nSIPHON has navigated to:")
   subprocess.call("pwd")
   print ("\n")
   subprocess.call("ls")
   print ("\n")
   print ("\nSIPHON has navigated to esedbToolsFolder:")
   subprocess.call("pwd")
   # if on Ubuntu, must be: ./esedbexport 
   subprocess.call("sudo " + "./esedbexport -m -t " + windowsEdbLocation, shell=True)

   # print "\nEdbTools Export Location: " + esedbToolsLocation + "/Windows.edb.export"
   # print ("\n")

edbExportLocation = tkFileDialog.askdirectory()

filesInExportFolder = []

for root, dirs, files in os.walk(edbExportLocation):
    for file in files:
        if 'SystemIndex_0A' in file:
            filesInExportFolder.append(os.path.join(root, file))
            sysIndexVariable = ''.join(filesInExportFolder)

# copy file from esedbtools/Windows.edb.export folder to desktop (big(ish) file)
shutil.copyfile(sysIndexVariable, "/home/si/Desktop/SystemIndex_0A")

csv.register_dialect('MyDialect', delimiter='\t',doublequote=False,quotechar='',lineterminator='\n',escapechar='',quoting=csv.QUOTE_NONE)
# End of adapted code

with open('/home/si/Desktop/SystemIndex_0A', 'rU') as csvfile:
    SysIndex = csv.reader(csvfile, 'MyDialect')

    headers = next(SysIndex, None)  

    for row in SysIndex:
    	if thumbcacheID in row:

            zip(headers, row)
            saveFileAs = raw_input('Where do you wish to save the file?: ')
            writer = csv.writer(open(saveFileAs, "w"))
            writer.writerows(zip(headers, row))
            print ("\n\nThumbcache_ID found. Please see output in SIPHON.csv")
            print ("\n\nReport:")
            a = row[31]
            realSystemItemUrl = a.replace('\\\\', "\\")
            # print "Your searched thumbcacheID: " + thumbcacheID
            print ("Location of original file:"), realSystemItemUrl
            fileType = row[253]
            print ("File Type:"), fileType
            print ("Information taken from System_ItemUrl and System_FileExtension Headers.\n")
csvfile.close()

# can remove desktop file if you want by uncommenting the line below
# os.remove("/home/si/Desktop/SystemIndex_0A")

print ("\nThank you for using SIPHON...\n")

#########################################
#######DEBUGGING SECTION BELOW###########
######################################### 

# New EDB: 
# 631278677cd4d2e3
# b014618486f9299e