#!/usr/bin/env python
import sys
import webbrowser
import time
#this is a standard python module
from fractions import Fraction
# Exif module (To install on Linux: 'apt-get install python-pyexiv2')
import pyexiv2
# Importing tkinter GUI
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os
import hashlib
import subprocess
from time import ctime

#######################
###    FUNCTIONS    ###
#######################

#Converts DMS GPS data to decimal
def dms_to_decimal(degrees, minutes, seconds, sign=' '):
	#Takes input from DMS tuple to do a conversion calculation, it also takes into
	# consideration the Ref so that if the locations are either S or W facing they are minus 
	# DMS to Degrees
	# Degrees/Minutes/Seconds
	# x = (Seconds/3600) + (Minutes/60) + Degrees
	return (-1 if sign[0] in 'SWsw' else 1) * (
        float(degrees)        +
        float(minutes) / 60   +
        float(seconds) / 3600
    )


# Function used later
def close_window():
	root.withdraw()
# Sets the size of Tkinter box
root = Tk()
root.geometry('255x150+300+300')
root.title("SPIES, 2014")
# Text when opening program
text = Text(root)
text.insert(INSERT, "Please browse to JPG file...")
text.pack()


a =("\n\n		    Simon's Portable iPhone")
b =("	  _....,_      			    _,...._")
c =("       _.-` _,..,_'.     		 .'_,..,_ `-._")
d =("	 _,-`/ o \ '.     S.P.I.E.S     .' / o \`-,_")
e =("	  '-.\___/.-`     		`-.\___/.-'")
f =("		  \n		  Exif-Extraction Software")

# Print SPIES logo before prompt
def printLogo():
	print a
	print b
	print c
	print d
	print e
	print f

FILESIZE_SLICING_LIMIT = 5000000 #bytes - 4.76837mb

oneLat = []
oneLong = []
imageFileNameStore = [] # Stores file names e.g fanta.jpg for KML file in TraP
listofHashes = [] # List of MD5 hashes for all photographs


# gives back the MD5 hash of the given file
# if the file is big, this slices the file
# to avoid to loading the whole file into RAM

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


########################
### END OF FUNCTIONS ###
########################

printLogo()

# Browse Button
answer = tkFileDialog.askopenfilename()
root.withdraw() 
imagefilename = answer

# The following line just lets me get the filename itself

storedFileName = os.path.basename(answer)

print 'IMAGE FILE NAME LIST BELOW'
print imageFileNameStore


#trying to catch the exceptions in case of problem with the file reading
try:
	# Straight from the python-pyexiv2 tutorial, http://tilloy.net/dev/pyexiv2/tutorial.html#reading-and-writing-exif-tags 
	# Reading in zthe file and get the metadata
	metadata = pyexiv2.metadata.ImageMetadata(imagefilename)
	metadata.read();
#trying to catch the exceptions in case of problem with the GPS data reading
	try:
		getMd5 = getFileHashMD5(imagefilename)
		# getting out the values from the metadata tags, see http://tilloy.net/dev/pyexiv2/tutorial.html#reading-and-writing-exif-tags
		#allexif = metadata.exif_keys
		#print allexif
		# Fixes here by Kieron Craggs - KieronCraggs.com
		declat = dms_to_decimal(*metadata.__getitem__("Exif.GPSInfo.GPSLatitude").value + [metadata.__getitem__("Exif.GPSInfo.GPSLatitudeRef").value]);
		declon = dms_to_decimal(*metadata.__getitem__("Exif.GPSInfo.GPSLongitude").value + [metadata.__getitem__("Exif.GPSInfo.GPSLongitudeRef").value]);
		#print declat
		#print declon
		#

		print "\nGPS EXIF data for " + os.path.normpath(imagefilename), "\n" 
  
		print "Latitude is:\t" + str(declat) # Gives latitude in standard format
		
		print "\n\nLongitude is:\t" + str(declon)

		
		#print "\n####################"
		#print "#For debugging only#"
		#print "####################"

	# 	# For Google Maps ONLY
	# 	print "\nLatitude:\t" + rippedLatitude
	# 	print "Longitude:\t" + rippedLongitude

	# 	# Turn longitude into digits for Google Earth
	# 	rippedLatitudeFirstSet = rippedLatitude[0:2]
	# 	rippedLatitudeSecondSet = rippedLatitude[2:5]
	# 	rippedLatitudeThirdSet = rippedLatitude[6:11]

	# 	print "\nFirst lat: " + rippedLatitudeFirstSet
	# 	print "Second lat: " + rippedLatitudeSecondSet
	# 	print "Third lat: " + rippedLatitudeThirdSet

	# 	# e.g 32.19 in: 53 48 32.19
	# 	latitudeDegrees = float(rippedLatitudeFirstSet)
	# 	latitudeMinutes = float(rippedLatitudeSecondSet)
	# 	latitudeSeconds = float(rippedLatitudeThirdSet)

	# 	# Converted to decimal so can now be sent to KML file
	# 	finalLatCoordToDecimal = str(latitudeDegrees + ((latitudeMinutes / 60) + (latitudeSeconds/3600)))

	# 	print "\nCalc for GE: " + finalLatCoordToDecimal

	# 	# As above but longitude
	# 	rippedLongitudeFirstSet = rippedLongitude[0:2]
	# 	rippedLongitudeSecondSet = rippedLongitude[2:4]
	# 	rippedLongitudeThirdSet = rippedLongitude[5:9]

	# 	print "\n\nFirst long: " + rippedLongitudeFirstSet
	# 	print "Second long: " + rippedLongitudeSecondSet
	# 	print "Third long: " + rippedLongitudeThirdSet

	# 	# e.g 32.19 in: 53 48 32.19
	# 	longitudeDegrees = float(rippedLongitudeFirstSet)
	# 	longitudeMinutes = float(rippedLongitudeSecondSet)
	# 	longitudeSeconds = float(rippedLongitudeThirdSet)

	# 	# Converted to decimal so can now be sent to KML file
	# 	finalLongCoordToDecimal = str(longitudeDegrees + ((longitudeMinutes / 60) + (longitudeSeconds/3600)))
			
	# 	# Code below removed for v6.0.5 - please read documentation
	# 	# oneLat.append(finalLatCoordToDecimal)
	# 	# oneLong.append(finalLongCoordToDecimal)
	# 	# listofHashes.append(md5Val)

	# # print ("One lat, one long\n\n")
	# # print oneLat
	# # print oneLong

		#print "\nCalc for GE: " + finalLongCoordToDecimal

		#print "####################"
		#print "# End of debugging #"
		#print "####################"

		print "\nMD5 Hash: " + md5Val
		# The stuff below is just for debugging. It shows what I ripped from the array
		# print '\n\n\n' + str(rippedLatitude) 
		# print '\n' + str(rippedLongitude) 

		if tkMessageBox.askyesno("SPIES, 2014", "Do you want to locate on Google Maps now?"):

			webbrowser.open("https://maps.google.co.uk/maps?q=%s,%s" % (declat,declon))
		
			print a
			print b
			print c
			print d
			print e
			print f
		else:
			print a
			print b
			print c
			print d
			print e
			print f
			root.quit()

		with open('spiesDir\spiesOutput.txt', 'w') as txt:
			txt.write('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\t\t\t\tS.P.I.E.S\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n' "\nYour scanned image location was: \n\n"  + os.path.normpath(imagefilename))
			txt.write('\n\nMD5 Hash is: ' + md5Val)
			txt.write('\n\nCoordinates: \n\nLatitude is: ' + str(declat))
			txt.write('\nLongitude is: ' + str(declon))
			txt.write('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
			txt.write('\nThank you for using S.P.I.E.S. \nS.P.I.E.S is free of charge and comes with no guarantee. Happy investigating.')
			# with automatically closes - no need for txt.close()

#########################################
# 		THE FOLLOWING IS NOT MY CODE 	#
#########################################

	except Exception, e:  # complain if the GPS reading went wrong, and print the exception
		print "Missing GPS info for " + imagefilename
		print e;
	
except Exception, e:   # complain if the GPS reading went wrong, and print the exception
	print "Error processing image " + imagefilename
	print e;

#######################################
# 		END OF BORROWED CODE 	 	  #
#######################################
print "\n\n\t\t Thank you for using SPIES!\n\t\t\t  Goodbye!\n\n"

#########################

 # T R A C E P L A CE  #
#########################

if tkMessageBox.askyesno("SPIES, 2014", "Do you want to use TraP to timeline photographs on Google Earth?"):
	pass
else:
	sys.exit(1)

import webbrowser, binascii, os, shutil, zipfile, time, os, zipfile

aa = " .     .       .  .   . .   .   . .    +  ."
bb = "   .     .  :     .    .. :. .___---------___."
cc = '        .  .   .    .  :.:. _".^ .^ ^.  \'.. :"-_. .'
dd = "     .  :       .  .  .:../:            . .^  :.:\."
ee = "         .   . :: +. :.:/: .   .    .        . . .:"
ff = "  .  :    .     . _ :::/:               .  ^ .  . .:"
gg = "   .. . .   . - : :.:./.       Sopia Suite      .  .:"
hh = "   .      .     . :..|:                    .  .  ^. .:|"
ii = "     .       . : : ..||        . Presents       . . !:|"
jj = "   .     . . . ::. ::\(                           . :)/"
kk = "  .   .     : . : .:.|. ######      TraP    .#######::|"
ll = "   :.. .  :-  : .:  ::|.#######           ..########:|"
mm = "  .  .  .  ..  .  .. :\ ########          :######## :/"
nn = "   .        .+ :: : -.:\ ########       . ########.:/"
oo = "     .  .+   . . . . :.:\. #######       #######..:/"
pp = "       :: . . . . ::.:..:.\           .   .   ..:/"
qq = "    .   .   .  .. :  -::::.\.       | |     . .:/"
rr = "       .  :  .  .  .-:.\":.::.\             ..:/"
ss = "  .      -.   . . . .: .:::.:.\.   _____  .:/"
tt = " .   .   .  :      : ....::_:..:\  \___/.  :/"
uu = "    .   .  .   .:. .. .  .: :.:.:\       :/"
vv = "      +   .   .   : . ::. :.:. .:.|\  .:/|"
ww = "      .         +   .  .  ...:: ..|  --.:|"
xx = ' .      . . .   .  .  . ... :..:.."(  ..)"'
yy = "  .   .       .      :  .   .: ::/  .  .::"

print aa
time.sleep( 0.1 )
print bb
time.sleep( 0.1 )
print cc
time.sleep( 0.1 )
print dd
time.sleep( 0.1 )
print ee
time.sleep( 0.1 )
print ff
time.sleep( 0.1 )
print gg
time.sleep( 0.1 )
print hh
time.sleep( 0.1 )
print ii
time.sleep( 0.1 )
print jj
time.sleep( 0.1 )
print kk
time.sleep( 0.1 )
print ll
time.sleep( 0.1 )
print mm
time.sleep( 0.1 )
print nn
time.sleep( 0.1 )
print oo
time.sleep( 0.1 )
print pp
time.sleep( 0.1 )
print qq
time.sleep( 0.1 )
print rr
time.sleep( 0.1 )
print ss
time.sleep( 0.1 )
print tt
time.sleep( 0.1 )
print uu
time.sleep( 0.1 )
print vv
time.sleep( 0.1 )
print ww
time.sleep( 0.1 )
print xx
time.sleep( 0.1 )
print yy
time.sleep( 0.1 )

#######################
###    FUNCTIONS    ###
#######################
#
def readExifFromPhoto(x):

	imagefilename = x
	


	# Found at: https://stackoverflow.com/questions/8384737/python-extract-file-name-from-path-no-matter-what-the-os-path-format
	storedFileName = os.path.basename(imagefilename)

	imageFileNameStore.append(storedFileName)


	#trying to catch the exceptions in case of problem with the file reading
	try:
		# Straight from the python-pyexiv2 tutorial, http://tilloy.net/dev/pyexiv2/tutorial.html#reading-and-writing-exif-tags 
		# Reading in the file and get the metadata
		metadata = pyexiv2.metadata.ImageMetadata(imagefilename)
		metadata.read();
	#trying to catch the exceptions in case of problem with the GPS data reading
		try:
			getFileHashMD5(imagefilename)
			# getting out the values from the metadata tags, see http://tilloy.net/dev/pyexiv2/tutorial.html#reading-and-writing-exif-tags
			latitude = metadata.__getitem__("Exif.GPSInfo.GPSLatitude")
			latitudeRef = metadata.__getitem__("Exif.GPSInfo.GPSLatitudeRef")
			longitude = metadata.__getitem__("Exif.GPSInfo.GPSLongitude")
			longitudeRef = metadata.__getitem__("Exif.GPSInfo.GPSLongitudeRef")
			
			# get the value of the tag, and make it a float
			alt = float(metadata.__getitem__("Exif.GPSInfo.GPSAltitude").value)

			# get human readable values
			latitude = str(latitude).split("=")[1][1:-1].split(" ");
			latitude = map(lambda f: str(float(Fraction(f))), latitude)
			latitude = latitude[0] + " " + latitude[1] + " " + latitude[2] + '"' + " " + str(latitudeRef).split("=")[1][1:-1]

			longitude = str(longitude).split("=")[1][1:-1].split(" ");
			longitude = map(lambda f: str(float(Fraction(f))), longitude)
			longitude = longitude[0] + " " + longitude[1] + " " + longitude[2] + '"' + " " + str(longitudeRef).split("=")[1][1:-1]


			print "\nGPS EXIF data for " + os.path.normpath(imagefilename), "\n" 
			# C:\Users\Simon\Desktop\spies.SimonsPortableIphoneExifExtractionSoftware\photo.JPG  (53)
			# print "Latitude:\t" + latitude,
			# 53.0 48.54 0.0
			print "Latitude is:\t" + latitude # Gives latitude in standard format

			rippedLatitude = str(int(float(latitude[0:2]))) + " " + str(latitude[5] + latitude[6] + (latitude[9] + latitude[10:15])) # Take coordinates out using array and turn into string variable
			
			print "Longitude is:\t" + longitude

			# In order to work with single digit beginning of longitudes, must be float FIRST then int, then finally string
			rippedLongitude = str(int(float(longitude[0:2]))) + " " + str(longitude[4] + longitude[5] + longitude[8] + longitude[9:14])
			
			print "\n####################"
			print "#For debugging only#"
			print "####################"
			# For Google Maps ONLY
			print "\nLatitude From Array:\t" + rippedLatitude
			print "Longitude From Array:\t" + rippedLongitude

			# Turn longitude into digits for Google Earth
			rippedLatitudeFirstSet = rippedLatitude[0:2]
			rippedLatitudeSecondSet = rippedLatitude[2:5]
			rippedLatitudeThirdSet = rippedLatitude[6:11]

			print "\nFirst lat: " + rippedLatitudeFirstSet
			print "Second lat: " + rippedLatitudeSecondSet
			print "Third lat: " + rippedLatitudeThirdSet

			# e.g 32.19 in: 53 48 32.19
			latitudeDegrees = float(rippedLatitudeFirstSet)
			latitudeMinutes = float(rippedLatitudeSecondSet)
			latitudeSeconds = float(rippedLatitudeThirdSet)

			global finalLatCoordToDecimalTwo

			# Converted to decimal so can now be sent to KML file
			finalLatCoordToDecimalTwo = str(latitudeDegrees + ((latitudeMinutes / 60) + (latitudeSeconds/3600)))

			print "\nCalc for GE: " + finalLatCoordToDecimalTwo

			# As above but longitude
			rippedLongitudeFirstSet = rippedLongitude[0:2]
			rippedLongitudeSecondSet = rippedLongitude[2:4]
			rippedLongitudeThirdSet = rippedLongitude[5:9]

			print "\nFirst long: " + rippedLongitudeFirstSet
			print "Second long: " + rippedLongitudeSecondSet
			print "Third long: " + rippedLongitudeThirdSet

			# e.g 32.19 in: 53 48 32.19
			longitudeDegrees = float(rippedLongitudeFirstSet)
			longitudeMinutes = float(rippedLongitudeSecondSet)
			longitudeSeconds = float(rippedLongitudeThirdSet)

			global finalLongCoordToDecimalTwo

			# Converted to decimal so can now be sent to KML file
			finalLongCoordToDecimalTwo = str(longitudeDegrees + ((longitudeMinutes / 60) + (longitudeSeconds/3600)))

			print "\nCalc for GE: " + finalLongCoordToDecimalTwo

			print "####################"
			print "# End of debugging #"
			print "####################"

		except Exception, e:  # complain if the GPS reading went wrong, and print the exception
			print "Missing GPS info for " + imagefilename
			print e;
		
	except Exception, e:   # complain if the GPS reading went wrong, and print the exception
		print "Error processing image " + imagefilename
		print e;

def Quit():
	sys.exit(1)

def kmzSaveCopyTreeVersionTwo():
	addPath = str(os.getcwd())
	global kmzFileLocation
	#kmzFileLocation = raw_input('\n\nWhere do you wish to save the output files? ')
	kmzFileLocation = os.path.join(addPath, 'output')
	# print 'CURRENT WORKING DIRECTORY\n'
	# print os.getcwd()	
	cpFrom = os.path.join(addPath, 'photoEvidence')
	cpTo = os.path.join(kmzFileLocation, 'files')
	print ("\nCopying files...")
	shutil.copytree(cpFrom, cpTo)
	print ("Copying complete...")
	examinedPhotoData()
	# kmzVersionThreePics()




def zipKML():
	# Sets the size of Tkinter box
	root = Tk()
	root.geometry('255x150+300+100')
	root.title("SPIES, 2014")
	# Text when opening program
	# text = Text(root)
	# text.insert(INSERT, "Please browse to JPG file...")
	# text.pack()
	# Ask user where to save KMZ file
	global saveFileAs
	saveFileAs = tkFileDialog.asksaveasfilename(parent=root,title="Save as...")
	zfName = (saveFileAs)
	foo = zipfile.ZipFile(zfName, 'w')
	foo.write("temp.kml")
	# Adding files from directory 'files'
	for root, dirs, files in os.walk('files'):
		for f in files:
			foo.write(os.path.join(root, f))
	foo.close()
	# Cleanup
	os.remove("temp.kml")
	shutil.rmtree('files')



# This function writes information about all the photographs
# that have been passed to TraP, such as timestamps and file hashes
 # Need to add modified accessed created timestamps too...
def examinedPhotoData():
		os.chdir(kmzFileLocation)
		print str(os.getcwd()) + 'Examined photos CWD'
		with open("trapRecord.txt",'w') as f:
			f.write("Trap Evidence Record\n\n")

			coordPairs = zip((-float(x) for x in oneLong), (float(x) for x in oneLat))

			increment = 0
			# print "\nFile Names In List: " + str(imageFileNameStore)
			# print "File Name Length: " + str(len(imageFileNameStore))
			# print "Latitude of File: " + str(oneLat)
			# print "Longitude List: " + str(oneLong)
			# print '\n\nList Of Hashes: \n' + str(listofHashes)
			timeStamp = ctime()
			while increment < len(imageFileNameStore):
				for coord in coordPairs:
					# Making use of string formatting to get MD5 hashes, file name and photograph location
					f.write("File Name: {}".format(imageFileNameStore[increment])) # Need to add file name here
					f.write("\nMD5 Hash: {}".format(listofHashes[increment]))
					increment = increment + 1
					print "\nincrement Loop 1: " + str(increment)
					for coord in coordPairs:
						f.write("\nLongitude: {}\nLatitude: {}".format(*coordPairs[increment-1]))
						f.write("\n\n")
						print "increment Loop 2: " + str(increment)
						break
				f.write("\nAll the data above was passed through TraP on: " + timeStamp)
		print ("\n\nRecord Created")
		kmzVersionThreePics()


def kmzVersionThreePics():
		#os.chdir(kmzFileLocation)

		with open("temp.kml",'w') as f:
			f.write('''<?xml version="1.0" encoding="UTF-8"?>
	<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
	<Document>
		<name>TracePlace</name>
		<open>1</open>
		<Style id="Photo">
			<IconStyle>
				<Icon>
					<!-- a KMZ file is a zip file re-named KMZ. 
					The image below is the icon image and stored
					in the files folder -->
					<href>..\icon\icon.jpg</href>
				</Icon>
			</IconStyle>
			<LineStyle>
				<width>0.75</width>
			</LineStyle>
		</Style>
	<Folder>''')


			coordPairs = zip((-float(x) for x in oneLong), (float(x) for x in oneLat))

			increment = 0
			print "Length of image file name list: " + str(len(imageFileNameStore)) + '\n'
			print "File Names In List: " + str(imageFileNameStore)
			print "\nLatitude List: " + str(oneLat)
			print "\nLongitude List: " + str(oneLong)
			print '\nList Of Hashes: \n' + str(listofHashes)

			while increment < len(imageFileNameStore):
				for coord in coordPairs:
					# Making use of string formatting to get MD5 hashes, file name and photograph location
					f.write("\n\n<Placemark>\n")
					f.write("\t<name>File Name: {}</name>\n".format(imageFileNameStore[increment])) # Need to add file name here
					f.write("\t\t<Snippet maxLines=\"0\"></Snippet>\n")
					f.write("\t\t\t<description>MD5 Hash: {}<![CDATA[<img src='./files/{}' width='400' height='300'>]]></description>\n".format(listofHashes[increment], imageFileNameStore[increment]))
					f.write("\t\t<styleUrl>#Photo</styleUrl>\n")
					f.write("\t<Point>\n")
					increment = increment + 1
					print "\nincrement Loop 1: " + str(increment)
					for coord in coordPairs:
						f.write("\t\t<coordinates>{}, {}</coordinates>\n".format(*coordPairs[increment-1]))
						f.write("\t</Point>\n")
						f.write("</Placemark>\n\n")
						print "increment Loop 2: " + str(increment)
						break

			f.write('''
				</Folder>
				</Document>
				</kml>''')
		zipKML()
		print ("\n\nTraP has successfully created a KMZ file for you at: " + kmzFileLocation)
		print ("Double clicking the KMZ file will open Google Earth (if installed + associated).")
		quit()


fileStore = []

def ripDirectory():
	close_window() # Stop un-necessary window pop-up
	# path to os.walk through
	pathToWalk = tkFileDialog.askdirectory()

	# how many iterations needed
	numberOfWalks = len(os.listdir(pathToWalk))
	print 'number of walks: ' + str(numberOfWalks)

	# 		# Add files into fileStore list
	# for root, dirs, files in os.walk(pathToWalk):
	# 	for file in files:
	# 		fileStore.append(os.path.join(root,file))

	# Remove thumbs.db file from list as this would break the script
	# if file exists, delete it 
	delThumbs = (os.path.normpath(pathToWalk + "\Thumbs.db"))
	if os.path.exists(delThumbs):
		os.remove(delThumbs)
	else:
		pass

	for root, dirs, files in os.walk(pathToWalk):
		for file in files:
			print os.listdir(pathToWalk)
			fileStore.append(os.path.join(root,file))

	# Now we've appended the files in the directory
	# Rip coordinates from photographs and append to lat, long and hash lists
	num = 0
	while num < numberOfWalks:
		for files in fileStore:
			print num
			readExifFromPhoto(os.path.normpath(fileStore[num-1])) # This -1 isn't affecting the num variable outside of this command
			num = num + 1
			oneLat.append(finalLatCoordToDecimalTwo) #These two lines append the ripped coordinates to the oneLat and oneLong lists
			oneLong.append(finalLongCoordToDecimalTwo) # so all of the photos we ripped are together
			listofHashes.append(md5Val)
		break
	kmzSaveCopyTreeVersionTwo()

		# Add files into fileStore list



def quit():
	sys.exit(0)
########################
### END OF FUNCTIONS ###
########################

root = Tk() # This creates a window, but it won't show up

label = Label(root, text="How many pictures do you wish to timeline using TraP", font=('Calibri', 12))
button1 = Button(root, text = "Multiple Pics", command = ripDirectory())
button2 = Button(root, text = "Quit", command = Quit)

label.pack()
button1.pack()
button2.pack()
root.mainloop() # This command will tell the window come out

# close_window()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~ DEBUGGING SECTION - IGNORE EVERYTHING IN THIS SECTION ~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~