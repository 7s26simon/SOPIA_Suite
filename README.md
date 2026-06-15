<h1>SOPIA_Suite</h1>
===========

A suite of digital forensic tools written in Python.

<h1>WHAT DOES IT DO?</h1>

SOPIA Suite includes the following:


*Duff - Duplicate File Finder
*FiBS - File Investigation Bitesize
*SHIFT - Simon's Hash Info Finder Tool
*SIPHON - SIPHON...
*SPIES - Simon's Portable iPhone Exif-extraction Software

SIPHON parses a Windows.edb file using Libesedb and then parses the results of that to get thumbcache information.

<h1>DEPENDENCIES</h1>

SOPIA Suite has a number of dependencies which need to be met before usage:

Python 3 (ensure `python3` is on your PATH).
libesedb (built from source; SIPHON only, Linux/Ubuntu).
tkinter (bundled with most Python 3 installs).
Pillow (`pip install Pillow`; used by SPIES for EXIF GPS extraction).

<h1>USAGE</h1>

To run the tool, open a terminal and type: `python3 sopiaSuiteMenu.py`

<h1>LICENSE INFORMATION</h1>

Libesedb (third party code) is used in this project (credit given in the source code). Code released under the GNU license.
