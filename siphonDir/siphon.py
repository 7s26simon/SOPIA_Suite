#!/usr/bin/env python3
"""SIPHON (part of SOPIA Suite).

Parses a Windows.edb file using libesedb, then searches the exported
SystemIndex for a given thumbcache ID and reports the original file's
location and type. Linux (Ubuntu) only.
"""

import os
import sys
import csv
import shutil
import platform
import subprocess
import contextlib
import tkinter as tk
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SIPHON_LOGO = r"""

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

                 """


@contextlib.contextmanager
def change_dir(new_path):
    """Temporarily change the working directory."""
    saved_path = os.getcwd()
    os.chdir(new_path)
    try:
        yield
    finally:
        os.chdir(saved_path)


def main():
    root = tk.Tk()
    root.geometry("255x150+300+100")
    root.title("SIPHON, 2014")
    root.withdraw()

    print(SIPHON_LOGO)

    os_type = platform.system()
    print(
        "You are using: "
        + os_type
        + "\n\nNote: SIPHON is only supported on Ubuntu.\nFor further information, "
        "please consult\nthe help files that came with SOPIA Suite."
    )
    if os_type != "Linux":
        print(
            "Sorry, SIPHON is only compatible with Linux. For more details, "
            "please see\nthe help files."
        )
        sys.exit(1)

    thumbcache_id = input(
        "\nPlease enter the thumbcacheID you\nwish to search the database for: "
    )

    cwd = os.getcwd()
    esedb_tools_location = os.path.join(cwd, "libesedb-20120102", "esedbtools")
    windows_edb_location = os.path.join(cwd, "evidence", "Windows.edb")

    print(esedb_tools_location + "     ESE TOOLS LOCATION\n")
    print(windows_edb_location + "     WINDOWS EDB FILE LOCATION")

    with change_dir(esedb_tools_location):
        print("\nSIPHON has navigated to:")
        subprocess.call(["pwd"])
        subprocess.call(["ls"])
        # On Ubuntu the export tool is invoked as ./esedbexport
        subprocess.call(
            ["sudo", "./esedbexport", "-m", "-t", windows_edb_location]
        )

    export_location = filedialog.askdirectory()
    if not export_location:
        sys.exit(1)

    sys_index_file = None
    for dirpath, _dirnames, filenames in os.walk(export_location):
        for filename in filenames:
            if "SystemIndex_0A" in filename:
                sys_index_file = os.path.join(dirpath, filename)
                break

    if not sys_index_file:
        print("Could not find a SystemIndex_0A file in the export folder.")
        sys.exit(1)

    # Work on a local copy of the (large) index file.
    local_index = os.path.join(BASE_DIR, "SystemIndex_0A")
    shutil.copyfile(sys_index_file, local_index)

    csv.register_dialect(
        "MyDialect",
        delimiter="\t",
        doublequote=False,
        quotechar="",
        lineterminator="\n",
        escapechar="",
        quoting=csv.QUOTE_NONE,
    )

    with open(local_index, "r", newline="") as csvfile:
        sys_index = csv.reader(csvfile, "MyDialect")
        headers = next(sys_index, None)

        for row in sys_index:
            if thumbcache_id in row:
                save_file_as = input("Where do you wish to save the file?: ")
                with open(save_file_as, "w", newline="") as out:
                    writer = csv.writer(out)
                    writer.writerows(zip(headers, row))

                print("\n\nThumbcache_ID found. Please see output in SIPHON.csv")
                print("\n\nReport:")
                real_system_item_url = row[31].replace("\\\\", "\\")
                print("Location of original file:", real_system_item_url)
                print("File Type:", row[253])
                print(
                    "Information taken from System_ItemUrl and "
                    "System_FileExtension headers.\n"
                )

    print("\nThank you for using SIPHON...\n")


if __name__ == "__main__":
    main()
