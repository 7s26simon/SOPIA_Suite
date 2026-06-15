#!/usr/bin/env python3
"""DuFF - Duplicate File Finder (part of SOPIA Suite).

Walks a user-selected directory, hashes every file with MD5 and reports
any files that share a hash (i.e. duplicates) to a text file.
"""

import os
import sys
from collections import defaultdict
from itertools import chain
import tkinter as tk
from tkinter import messagebox, filedialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sopiaCore import get_file_hash_md5

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "outPut.txt")

LOGO = r"""
     _.._..,_,_   DDDD    UU   UU  FFFFFF   FFFFFF
    (          ) D    DD  UU   UU  FF       FF
     ]~,"-.-~~[  D     D  UU   UU  FF       FF
   .=])' (;  ([  D     D  UU   UU  FFFFFF   FFFFFF
   | ]::\ '    [ D    D   UU   UU  FF       FF
   '=]): .)  ([  DDDDD    UUUUUUU  FF       FF
     |:: '    |
      ~~----~~     Duplicate File Finder, SOPIA Suite
"""


def main():
    print(LOGO)

    # Sets up the Tkinter prompt window.
    root = tk.Tk()
    root.geometry("255x150+300+100")
    root.title("DuFF, 2014")
    text = tk.Text(root)
    text.insert(tk.INSERT, "Please browse to folder you wish to search...")
    text.pack()

    search_dir = filedialog.askdirectory()
    if not search_dir:
        sys.exit(1)

    # Map each hash to the list of files that produced it.
    file_dict = defaultdict(list)

    with open(OUTPUT_FILE, "w") as out:
        out.write(LOGO)
        out.write("\n\n\n\n\tMD5 Hash\t\t\t\tFilepath\n\n")

        for dirname, _dirnames, filenames in os.walk(search_dir):
            for filename in filenames:
                fullname = os.path.join(dirname, filename)
                h_md5 = get_file_hash_md5(fullname)
                file_dict[h_md5].append(fullname)
                out.write("\n" + h_md5 + " " + os.path.normpath(fullname))

        # Any hash mapping to more than one file indicates duplicates.
        duplicates = [
            os.path.normpath(path)
            for path in chain.from_iterable(
                files for files in file_dict.values() if len(files) > 1
            )
        ]

        out.write("\n\n\nDuplicate Files: \n\n%s" % "\n".join(duplicates))
        out.write(
            "\n\nPlease note: If the space above is empty, no duplicates were found."
        )
        out.write("\n\nThank you for using DuFF, part of SOPIA Suite.\n")

    print("\nComplete dictionary of hashes + files:\n")
    print(dict(file_dict))

    print(
        "\n\nDuFF has finished scanning your directory. It is strongly recommended "
        "that you\ngo to the DuFF directory and analyze the results manually.\n\n"
        "Thank you for using DuFF.\n"
    )

    messagebox.showinfo("DuFF, 2014", "DuFF has finished scanning your directory.")

    if messagebox.askyesno(
        "DuFF, 2014",
        "\n\nNote: DuFF has created a copy of your search in the DuFF folder.\n\n"
        "Do you wish to view this file in the terminal now?",
    ):
        with open(OUTPUT_FILE, "r") as fo:
            print(fo.read())

    messagebox.showinfo("DuFF, 2014", "Thank you for using DuFF, Goodbye!")
    root.destroy()
    sys.exit(0)


if __name__ == "__main__":
    main()
