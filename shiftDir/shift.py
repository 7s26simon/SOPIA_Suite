#!/usr/bin/env python3
"""SHIFT - Simon's Hash Info Finder Tool (part of SOPIA Suite).

Hashes every file in a chosen directory (MD5 and SHA-1) and reports any
file whose hash appears in a known-hash list ('hashfile').
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sopiaCore import get_file_hash_md5, get_file_hash_sha1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HASH_FILE = os.path.join(BASE_DIR, "hashfile")
OUTPUT_FILE = os.path.join(BASE_DIR, "shiftOutput.txt")

LOGO = (
    "  \\____            ____ \n"
    "   \\   \\           \\   \\ \n"
    "    \\SMC\\_____      \\   \\ \n"
    "     \\...~-__()______\\___\\_____________________ \n"
    "      \\        Simon's Hash Info Finder Tool___\\ \n"
    "       \\     oo ooooooooooooooooooooo o o  |_O__\\_ \n"
    "        ~~--_________/~~~/________________________) \n"
    "             |      /   /()                  | \n"
    "             0     /   /()                   0 \n"
    "                  /___/                         \n\n"
    "\t\tSHIFT Results Below\n\n"
)


def main():
    print(LOGO)

    root = tk.Tk()
    root.geometry("255x150+300+100")
    root.title("SHIFT, 2014")
    text = tk.Text(root)
    text.insert(tk.INSERT, "Please browse to folder you wish to scan...")
    text.pack()

    search_dir = filedialog.askdirectory()
    if not search_dir:
        sys.exit(1)

    try:
        with open(HASH_FILE, "r") as hash_f:
            hashes = hash_f.read()
    except IOError:
        print("cannot open file: ", HASH_FILE)
        sys.exit(1)

    if not os.path.isdir(search_dir):
        print("cannot find search dir: ", search_dir)
        sys.exit(1)

    num_md = 0
    num_sha = 0

    with open(OUTPUT_FILE, "w") as out:
        out.write(LOGO)

        for dirname, _dirnames, filenames in os.walk(search_dir):
            for filename in filenames:
                fullname = os.path.join(dirname, filename)

                h_md5 = get_file_hash_md5(fullname)
                if h_md5 in hashes:
                    num_md += 1
                    out.write("\n\nMD5 Hash Match: " + h_md5)
                    out.write("\nFile Location : " + os.path.normpath(fullname))
                    print("\nMD5 match: ", h_md5, os.path.normpath(fullname), "\n")

                h_sha1 = get_file_hash_sha1(fullname)
                if h_sha1 in hashes:
                    num_sha += 1
                    out.write("\n\nSHA1 Hash Match: " + h_sha1)
                    out.write("\nFile Location  : " + os.path.normpath(fullname))
                    print("SHA1 match  : ", h_sha1, os.path.normpath(fullname), "\n")

        out.write("\n\n\nFound %d MD5 match(es)" % num_md)
        out.write("\nFound %d SHA-1 match(es)" % num_sha)
        out.write("\n\n\nIf the space above is blank, SHIFT found 0 MD5 | SHA-1 matches.")
        out.write("\n\n\n\t\tThank you for using SHIFT!")

    messagebox.showinfo(
        "SHIFT, 2014",
        "\nFound %d MD5 match(es).\n\nFound %d SHA-1 match(es).\n\n"
        "Thank you for using SHIFT!\n\nPlease note: results have been created "
        "in the SHIFT directory\nfilename: %s" % (num_md, num_sha, OUTPUT_FILE),
    )

    print("File results can be found in the SHIFT directory, file: ", OUTPUT_FILE)

    if messagebox.askyesno(
        "SHIFT, 2014", "Do you wish to view this file in the terminal now?"
    ):
        with open(OUTPUT_FILE) as my_txt:
            print(my_txt.read())
    else:
        print("\nThank you for using SHIFT! Goodbye!\n")


if __name__ == "__main__":
    main()
