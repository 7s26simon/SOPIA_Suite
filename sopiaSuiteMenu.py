#!/usr/bin/env python3
"""SOPIA Suite launcher menu.

Presents a small Tkinter window that lets the user launch any of the
SOPIA Suite tools. Each tool runs as a separate Python process.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

# Directory this script lives in, so the tools can be found regardless
# of the current working directory or operating system.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def launch(*path_parts):
    """Launch a tool in a new process using the same Python interpreter."""
    script = os.path.join(BASE_DIR, *path_parts)
    proc = subprocess.Popen([sys.executable, script])
    root.destroy()
    proc.wait()


def call_duff():
    launch("duffDir", "duff.py")


def call_fibs():
    launch("fibsDir", "fibs.py")


def call_shift():
    launch("shiftDir", "shift.py")


def call_spies():
    launch("spiesDir", "spies.py")


def call_siphon():
    messagebox.showinfo(
        "SIPHON",
        "SIPHON is only compatible with Linux (Ubuntu).\n"
        "Please run it manually on Ubuntu.",
    )


def call_help():
    """Open the bundled CHM help file (Windows only)."""
    help_dir = os.path.join(BASE_DIR, "HelpFiles")
    chm = os.path.join(help_dir, "sopiaChm.chm")
    if not os.path.exists(chm):
        messagebox.showinfo("Help", "Help file could not be found.")
        return
    try:
        subprocess.Popen(["hh.exe", chm])
    except OSError:
        messagebox.showinfo(
            "Help", "Help files can only be opened on Windows (hh.exe)."
        )


def call_exit():
    print("\nThank you for using SOPIA Suite\n\tGoodbye!\n")
    root.destroy()
    sys.exit(0)


root = tk.Tk()
root.title("SOPIA Suite, 2014")
root.geometry("255x255+550+220")

text = tk.Text(root)
text.insert(tk.INSERT, "Please select which tool\nyou wish to use...")

buttons = [
    ("DUFF", call_duff),
    ("FIBS", call_fibs),
    ("SHIFT", call_shift),
    ("SPIES", call_spies),
    ("SIPHON", call_siphon),
    ("HELP FILES", call_help),
    ("EXIT", call_exit),
]

for label, command in buttons:
    tk.Button(root, text=label, relief=tk.FLAT, command=command).pack()

text.pack()
root.mainloop()
