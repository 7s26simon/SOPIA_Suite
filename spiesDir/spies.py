#!/usr/bin/env python3
"""SPIES - Simon's Portable iPhone Exif-extraction Software (part of SOPIA Suite).

Reads GPS EXIF data from a photograph and reports its decimal latitude /
longitude and MD5 hash, optionally plotting it on Google Maps. The TraP
mode timelines a folder of photographs into a KMZ file for Google Earth.

GPS extraction uses Pillow (PIL):  pip install Pillow
"""

import os
import sys
import time
import zipfile
import shutil
import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog

from PIL import Image
from PIL.ExifTags import GPSTAGS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sopiaCore import get_file_hash_md5, dms_to_decimal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_TXT = os.path.join(BASE_DIR, "spiesOutput.txt")

SPIES_LOGO = r"""

		    Simon's Portable iPhone
	  _....,_      			    _,...._
       _.-` _,..,_'.     		 .'_,..,_ `-._
	 _,-`/ o \ '.     S.P.I.E.S     .' / o \`-,_
	  '-.\___/.-`     		`-.\___/.-'

		  Exif-Extraction Software
"""

TRAP_LOGO = r"""
 .     .       .  .   . .   .   . .    +  .
   .     .  :     .    .. :. .___---------___.
        .  .   .    .  :.:. _".^ .^ ^.  '.. :"-_. .
     .  :       .  .  .:../:            . .^  :.:\.
         .   . :: +. :.:/: .   .    .        . . .:
  .  :    .     . _ :::/:               .  ^ .  . .:
   .. . .   . - : :.:./.       Sopia Suite      .  .:
   .      .     . :..|:                    .  .  ^. .:|
     .       . : : ..||        . Presents       . . !:|
   .     . . . ::. ::\(                           . :)/
  .   .     : . : .:.|. ######      TraP    .#######::|
   :.. .  :-  : .:  ::|.#######           ..########:|
  .  .  .  ..  .  .. :\ ########          :######## :/
   .        .+ :: : -.:\ ########       . ########.:/
     .  .+   . . . . :.:\. #######       #######..:/
       :: . . . . ::.:..:.\           .   .   ..:/
    .   .   .  .. :  -::::.\.       | |     . .:/
       .  :  .  .  .-:.\":.::.\             ..:/
  .      -.   . . . .: .:::.:.\.   _____  .:/
 .   .   .  :      : ....::_:..:\  \___/.  :/
    .   .  .   .:. .. .  .: :.:.:\       :/
      +   .   .   : . ::. :.:. .:.|\  .:/|
      .         +   .  .  ...:: ..|  --.:|
 .      . . .   .  .  . ... :..:.."(  ..)"
  .   .       .      :  .   .: ::/  .  .::
"""


def get_gps_coordinates(image_path):
    """Return (latitude, longitude) in decimal degrees, or None if absent."""
    with Image.open(image_path) as img:
        exif = img.getexif()
        # 0x8825 is the GPSInfo IFD pointer tag.
        gps_ifd = exif.get_ifd(0x8825)

    if not gps_ifd:
        return None

    gps = {GPSTAGS.get(tag, tag): value for tag, value in gps_ifd.items()}
    try:
        lat = dms_to_decimal(gps["GPSLatitude"], gps["GPSLatitudeRef"])
        lon = dms_to_decimal(gps["GPSLongitude"], gps["GPSLongitudeRef"])
    except KeyError:
        return None
    return lat, lon


def single_image_mode():
    """Extract GPS + MD5 from one user-selected image."""
    root = tk.Tk()
    root.geometry("255x150+300+300")
    root.title("SPIES, 2014")
    text = tk.Text(root)
    text.insert(tk.INSERT, "Please browse to JPG file...")
    text.pack()

    image_path = filedialog.askopenfilename()
    root.withdraw()
    if not image_path:
        return

    md5_val = get_file_hash_md5(image_path)
    coordinates = get_gps_coordinates(image_path)

    if coordinates is None:
        print("Missing GPS info for " + image_path)
        messagebox.showinfo("SPIES, 2014", "No GPS EXIF data found in this image.")
        root.destroy()
        return

    declat, declon = coordinates
    print("\nGPS EXIF data for " + os.path.normpath(image_path), "\n")
    print("Latitude is:\t" + str(declat))
    print("Longitude is:\t" + str(declon))
    print("\nMD5 Hash: " + md5_val)

    if messagebox.askyesno("SPIES, 2014", "Do you want to locate on Google Maps now?"):
        webbrowser.open("https://maps.google.co.uk/maps?q=%s,%s" % (declat, declon))

    border = (
        "~" * 77 + "\n" + "x" * 79 + "\n" + "~" * 77 + "\n"
    )
    with open(OUTPUT_TXT, "w") as txt:
        txt.write(border + "\t\t\t\tS.P.I.E.S\n" + border + "\n")
        txt.write("\nYour scanned image location was: \n\n" + os.path.normpath(image_path))
        txt.write("\n\nMD5 Hash is: " + md5_val)
        txt.write("\n\nCoordinates: \n\nLatitude is: " + str(declat))
        txt.write("\nLongitude is: " + str(declon))
        txt.write("\n\n" + border + "\n")
        txt.write(
            "\nThank you for using S.P.I.E.S.\n"
            "S.P.I.E.S is free of charge and comes with no guarantee. "
            "Happy investigating."
        )

    root.destroy()


def _print_logo_animated(logo):
    for line in logo.splitlines():
        print(line)
        time.sleep(0.05)


def build_kmz(photos, kmz_path):
    """Build a KMZ (zipped KML + photos) from a list of (path, lat, lon, md5)."""
    work_dir = os.path.join(BASE_DIR, "_trap_build")
    files_dir = os.path.join(work_dir, "files")
    os.makedirs(files_dir, exist_ok=True)

    kml_path = os.path.join(work_dir, "doc.kml")
    placemarks = []
    for path, lat, lon, md5_val in photos:
        name = os.path.basename(path)
        shutil.copy(path, os.path.join(files_dir, name))
        placemarks.append(
            "\n<Placemark>\n"
            "\t<name>File Name: {name}</name>\n"
            "\t\t<description>MD5 Hash: {md5}"
            "<![CDATA[<img src='./files/{name}' width='400' height='300'>]]>"
            "</description>\n"
            "\t<Point>\n"
            "\t\t<coordinates>{lon},{lat}</coordinates>\n"
            "\t</Point>\n"
            "</Placemark>\n".format(name=name, md5=md5_val, lat=lat, lon=lon)
        )

    kml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
        "<Document>\n\t<name>TracePlace</name>\n\t<open>1</open>\n<Folder>\n"
        + "".join(placemarks)
        + "</Folder>\n</Document>\n</kml>\n"
    )
    with open(kml_path, "w") as f:
        f.write(kml)

    with zipfile.ZipFile(kmz_path, "w", zipfile.ZIP_DEFLATED) as kmz:
        kmz.write(kml_path, "doc.kml")
        for name in os.listdir(files_dir):
            kmz.write(os.path.join(files_dir, name), os.path.join("files", name))

    shutil.rmtree(work_dir)


def trap_mode():
    """Timeline a folder of photographs into a KMZ file for Google Earth."""
    _print_logo_animated(TRAP_LOGO)

    photo_dir = filedialog.askdirectory(title="Select folder of photographs")
    if not photo_dir:
        return

    photos = []
    for dirpath, _dirnames, filenames in os.walk(photo_dir):
        for filename in filenames:
            if filename.lower() == "thumbs.db":
                continue
            path = os.path.join(dirpath, filename)
            coordinates = get_gps_coordinates(path)
            if coordinates is None:
                print("Missing GPS info for " + path)
                continue
            lat, lon = coordinates
            md5_val = get_file_hash_md5(path)
            photos.append((path, lat, lon, md5_val))
            print("Added %s (%s, %s)" % (os.path.basename(path), lat, lon))

    if not photos:
        messagebox.showinfo("SPIES, 2014", "No geotagged photographs were found.")
        return

    kmz_path = filedialog.asksaveasfilename(
        title="Save KMZ as...", defaultextension=".kmz"
    )
    if not kmz_path:
        return

    build_kmz(photos, kmz_path)
    print("\n\nTraP has successfully created a KMZ file for you at: " + kmz_path)
    print("Double clicking the KMZ file will open Google Earth (if installed).")


def main():
    _print_logo_animated(SPIES_LOGO)
    single_image_mode()

    print("\n\n\t\t Thank you for using SPIES!\n\t\t\t  Goodbye!\n")

    if messagebox.askyesno(
        "SPIES, 2014",
        "Do you want to use TraP to timeline photographs on Google Earth?",
    ):
        trap_mode()
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
