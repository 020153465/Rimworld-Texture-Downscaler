# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 04:28:27 2021

@author: Saito8546
"""
#####################
# Importing Library #
#####################
import os

from shutil import copyfile
from tkinter import simpledialog, messagebox

###################
# GLOBAL VARIABLE #
###################
PRINT_INFO = None # Editable from the main file, not here #
BAK_CODE_DICT = {1: "Backing up known texture.\n"
                 "Will overwrite last one\n",
                 2: "Restoring from backup known texture.\n"
                 "Will overwrite current texture.\n",
                 3: "Deleting back up texture.\n"
                 "All texture file.RTHBak will be gone.\n"}

"""________________
  /               /
 / BACKUP EDITOR /
/_______________/"""


#==============================================#
# Asking for confirmation before taking action #
def confirmation(t_list, opcode):
    MsgBox = messagebox.askquestion("Confirmation",
                                   f"{BAK_CODE_DICT[opcode]}"
                                    "Do you want to continue?",
                                    icon = 'warning')
    if MsgBox == "yes":
        if opcode == 1:
            return backup(t_list)
        elif opcode == 2:
            return restore(t_list)
        else:
            return delete(t_list)


#=================================================#
# Make a 2nd copy of every texture as file.RTHBak #
def backup(t_list):
    if PRINT_INFO == True:
        print("[INFO]: Doing backup ...")
    count = 0
    for file in t_list:
        copyfile(file, f"{file}.RTHBak")
        count += 1
    if PRINT_INFO == True:
        print(f"[INFO]: Backup: {count}/{len(t_list)} files")
    return count


#=======================================================#
# Copy texture files.RTHBak back to normal texture file #
def restore(t_list):
    if PRINT_INFO == True:
        print("[INFO]: Restoring from backup ...")
    restore = 0
    for file in t_list:
        try:
            copyfile(f"{file}.RTHBak", file)
            restore += 1
        except FileNotFoundError:
            pass
    if PRINT_INFO == True:
        print(f"[INFO]: Files restored: {restore}/{len(t_list)} files")
    return restore


#=================================#
# Delete all texture files.RTHBak #
def delete(t_list):
    if PRINT_INFO == True:
        print("[INFO]: Deleting backup ...")
    delete = 0
    for file in t_list:
        try:
            os.remove(f"{file}.RTHBak")
            delete += 1
        except FileNotFoundError:
            pass
    if PRINT_INFO == True:
        print(f"[INFO]: Deleted backup: {delete}/{len(t_list)} files")
    return delete


#=================================================#
# Prompt the "What to do dialog", return int code #
def get_opcode():
    global PRINT_INFO
    if PRINT_INFO == True:
        print("[INFO]: Getting backup operational code")

    try:
        mode = simpledialog.\
            askinteger(title="Backup Editor Menu ?",
                      prompt="Input operational code for Backup Editor:\n"
                             "[1 = Backup Texture] - "
                             "(Will copy a 2nd texture file for every detected texture file)\n"
                             "[2 = Restore Texture from backup] - "
                             "(Revert texture files back to last backup state)\n"
                             "[3 = Delete Backup] "
                             "(Remove all backup texture files)\n"
                             "[Anything else = Return to main menu]\n" +
                             "_" * 100 + "\n"
                             "Note: All backup files will be created inside the Mods folder\n")
        if mode is None:
            return -1
        if mode >= 1 and mode <= 3:
            return mode

    # Something went wrong section #
    # Expected exception #
    except (ValueError, TypeError) as e:
        messagebox.showinfo("[INFO]",
                           f"OPCODE: {mode}\n"
                           f"{e}\n"
                            "Return to main menu !")
    # WTH happened exception #
    except Exception as e:
        messagebox.showerror("[ERROR]",
                            f"OPCODE: Woah wth just happened ?\n"
                            f"{e}\n"
                             "Return to main menu !")
    return -1


def main(t_list, info):
    global PRINT_INFO
    PRINT_INFO = info
    # UI Loop #
    while True:
        # Get code #
        opcode = get_opcode()
        if opcode == -1:
            break

        # Ask confirmation, parse code into function, do stuff #
        result = confirmation(t_list, opcode)
        if result is not None:
            messagebox.showinfo("Operation Result",
                                f"Finished {BAK_CODE_DICT[opcode].split(' ')[0]} " # Yes there's no new line here
                                f"{result}/{len(t_list)} files")


if __name__ == "__main__":
    print("Run this script from \"Rimworld Texture Helper.py\" instead")


