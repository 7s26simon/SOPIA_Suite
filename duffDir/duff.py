import sys, os, hashlib
from collections import defaultdict
from itertools import chain
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFileDialog

#######################
###    FUNCTIONS    ###
#######################

def close_window():
    root.destroy()

a = ("""    
         _.._..,_,_   DDDD    UU   UU  FFFFFF   FFFFFF     
        (          ) D    DD  UU   UU  FF       FF        
         ]~,\"-.-~~[  D     D  UU   UU  FF       FF         
       .=])\' (;  ([  D     D  UU   UU  FFFFFF   FFFFFF 
       | ]::\ '    [ D    D   UU   UU  FF       FF      
       \'=]): .)  ([  DDDDD    UUUUUUU  FF       FF       
         |:: \'    |                                          
          ~~----~~     Duplicate File Finder, SOPIA Suite  
      """)

def printLogo():
  print a

# Sets the size of Tkinter box
root = Tk()
root.geometry('255x150+300+100')
root.title("DuFF, 2014")
# Text when opening program
text = Text(root)
text.insert(INSERT, "Please browse to folder you wish to search...")
text.pack()

fileSliceLimitation = (5 * 1024*1024) #megabytes


def getFileHashMD5(filename):
     retval = 0;
     filesize = os.path.getsize(filename)

     if filesize > fileSliceLimitation:
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

     return retval


########################
### END OF FUNCTIONS ###
########################


# Call the print logo function
printLogo()

searchdirpath = tkFileDialog.askdirectory()
if searchdirpath == "":
  sys.exit(1)

print "\n"

text_file = open('duffDir\outPut.txt', 'w')

text_file.write(a)



file_dict = defaultdict(list) 



#  syntax for dictionaries in Python: dictionaryName[key] = value

text_file.write("\n\n\n\n\tMD5 Hash\t\t\t\tFilepath\n\n")

# Code below is scanning the directory the user chosen and applying an MD5
# hash to each file. The final line in the loop then writes the MD5 hash to a
# text file, followed by the name of that hash for easy analysis

for dirname, dirnames, filenames in os.walk(searchdirpath):
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        h_md5 = getFileHashMD5 (fullname)


        # This line appends file name and hash to the list file_dict
        file_dict[getFileHashMD5(fullname)].append(fullname)


        #print h_md5 + " " + fullname
        text_file.write("\n" + h_md5 + " " + os.path.normpath(fullname))   


print '\nComplete dictionary of hashes + files:\n'
print file_dict


# My original line didn't let me loop through it because it was a dictionary.
# So I had to convert it to a string using the chain from itertools module

duplicates = map(os.path.normpath, chain.from_iterable(files for files in file_dict.values() if len(files) > 1))

###################################
#     END OF ADAPTED CODE         #
###################################

# Now I've looped through the dictionary, I print out the duplicate files
text_file.write("\n\n\nDuplicates Files: \n\n%s" % '\n'.join(duplicates))

text_file.write("\n\nPlease note: If space above is empty, no duplicates were found.")
text_file.write("\n\nThank you for using DuFF, part of SOPIA Suite.\n")
text_file.close()

print "\n\nDuFF has finished scanning your directory. It is strongly recommended that you\ngo to the duff directory (cd duff+tab) and analyze the results manually.\n\nThank you for using DuFF.\n"

tkMessageBox.showinfo("DuFF, 2014","DuFF has finished scanning your directory.")

if tkMessageBox.askyesno("DuFF, 2014","\n\nNote: DuFF has created a copy of your search in the DuFF folder.\n\nDo you wish to view this file in the terminal now?"):
	with open('duffDir\outPut.txt', 'r+') as fo:
		data = fo.read() #Read whole file into data
	print data
	# Close the file
	fo.close()
	tkMessageBox.showinfo("DuFF, 2014","Thank you for using DuFF, Goodbye!")
else:
	tkMessageBox.showinfo("DuFF, 2014","Thank you for using DuFF, Goodbye!")
	close_window()


sys.exit(0)