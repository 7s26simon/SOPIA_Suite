#!/usr/bin/env python3
"""FIBS - File Investigation Bite-Size (part of SOPIA Suite).

Walks a chosen directory and produces an HTML report listing, for every
file, its name, owner UID, path, size and MD5 / SHA-1 hashes. Optionally
captures a snapshot of the machine's live processes (Linux / macOS).
"""

import os
import sys
import platform
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sopiaCore import get_file_hash_md5, get_file_hash_sha1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_HTML = os.path.join(BASE_DIR, "output.html")

LOGO = r"""
          _,.-------.,_
      ,;~'             '~;,
    ,;                     ;,
   ;     Welcome to FIBS     ;
  ,'   (file investigation    ',
 ,;         bite-size)         ;
 ; ;      .           .      ; ;
 | ;   ______       ______   ; |
 |  `/~'     ~' . '~     '~\'  |
 |  ~  ,-~~~^~, | ,~^~~~-,  ~  |
  |   | SIMONS}:{  SUITE |   |
  |   l SOPIA / | \  2014!   |
  .~  (__,.--' .^. '--.,__)  ~.
  |     ---;' / | \ `;---     |
   \__.       \/^\/       .__/
    V| \                 / |V
     | |T~\___!___!___/~T| |
     | |`IIII_I_I_I_IIII'| |
     |  \,III I I I III,/  |
     \    `~~~~~~~~~~'    /
        \   .       .   /
          \.    ^    ./
            ^~~~^~~~^
"""


def capture_live_processes(root):
    """Offer to capture a snapshot of running processes (non-Windows)."""
    if not messagebox.askyesno(
        "FIBS, 2014", "Do you want to capture live processes of this machine?"
    ):
        return

    with os.popen("ps -Af") as proc:
        process_output = proc.read()
    captured_at = datetime.now()

    location = filedialog.asksaveasfilename(
        parent=root,
        filetypes=[("html", "*.html")],
        title="Save the file as...",
    )
    if not location:
        return

    with open(location, "w") as f:
        f.write(
            "Below is a list of processes captured live at the following "
            "date + time: " + str(captured_at) + "\n\n"
        )
        f.write(process_output)
        f.write("\n\n\nThank you for using FIBS!\nFIBS is part of SOPIA Suite, 2014.")


def main():
    print(LOGO)

    root = tk.Tk()
    root.geometry("255x150+300+100")
    root.title("FIBS, 2014")
    root.withdraw()

    print("Detecting OS...")
    os_type = platform.system()
    print("OS Detected: " + os_type)

    # Live-process capture is only meaningful on Unix-like systems.
    if os_type != "Windows":
        capture_live_processes(root)
        if not messagebox.askyesno(
            "FIBS, 2014", "Do you wish to continue using FIBS?"
        ):
            messagebox.showinfo("FIBS, 2014", "\n\nThank you for using FIBS! Goodbye!\n")
            sys.exit(0)

    search_dir = filedialog.askdirectory()
    if not search_dir:
        messagebox.showinfo("FIBS, 2014", "\n\nThank you for using FIBS! Goodbye!\n")
        sys.exit(0)

    print("\n\nFolder Selected: " + os.path.normpath(search_dir))

    start = datetime.now()
    file_id = 1000

    with open(OUTPUT_HTML, "w") as f:
        f.write("<html> \n\n")
        f.write('\n<img src="./logo/fibsLogo.png" alt="logo"> <br>')
        f.write(
            "\n\n\nYou searched the following directory: \n"
            + os.path.normpath(search_dir)
            + "\n\n\n"
        )
        f.write("<br><br>Results for custom search: \n\n\n")

        for dirname, _dirnames, filenames in os.walk(search_dir):
            for filename in filenames:
                path_name = os.path.join(dirname, filename)
                md5_val = get_file_hash_md5(path_name)
                sha_val = get_file_hash_sha1(path_name)
                file_stat = os.stat(path_name)

                f.write("<p>")
                f.write("<br>FIBS File Identifier: %d" % file_id)
                f.write("<br>\n%d File Name: %s" % (file_id, filename))
                f.write("<br>\n%d UID: %s\n" % (file_id, file_stat.st_uid))
                f.write(
                    "<br>%d Enclosing Directory: %s\n"
                    % (file_id, os.path.normpath(path_name))
                )
                f.write("<br>%d Size in Bytes: %d\n\n" % (file_id, file_stat.st_size))
                f.write("<br>%d File Hash (MD5): %s" % (file_id, md5_val))
                f.write("<br>%d File Hash (SHA1): %s" % (file_id, sha_val))
                f.write("</p>")
                file_id += 1

        f.write("\n\n</html>")

    finished = datetime.now()
    difference = finished - start
    print("Difference is: " + str(difference))

    messagebox.showinfo(
        "FIBS, 2014",
        "\t\tFinished Processing Data\n\n\tStarted processing data at: "
        + str(start)
        + "\n\nFind results at: \n\n"
        + str(OUTPUT_HTML)
        + "\n\n\n\tTime taken to scan directory: (H,M,S,MS) "
        + str(difference),
    )

    with open(OUTPUT_HTML, "a") as f:
        f.write("FIBS Stats: ")
        f.write("Started processing data at: " + str(start))
        f.write("<br>Finished processing data at: " + str(finished))
        f.write("<br>Total time taken to scan directory: (H,M,S,MS) " + str(difference))
        f.write("<br><br>Thank you for using FIBS!")

    print("\n\nResults saved at following location: " + OUTPUT_HTML)
    print("\n\nThank you for using FIBS")
    messagebox.showinfo("FIBS, 2014", "Thank you for using FIBS, Goodbye!")


if __name__ == "__main__":
    main()
