# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 04:28:27 2021

@author: Saito8546
"""
#####################
# Importing Library #
#####################
import os
import datetime

from shutil import copyfile
from tkinter import Tk, simpledialog, messagebox
from tkinter.ttk import Progressbar
###################
# GLOBAL VARIABLE #
###################
PRINT_INFO = None # Editable from the main file, not here #
BAK_CODE_DICT = {1: "Backing up known texture.\n"
                 "Will overwrite last one\n",
                 2: "Restoring from backup.\n"
                 "Will overwrite current texture.\n",
                 3: "Deleting backup texture.\n"
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

    return None


#=================================================#
# Make a 2nd copy of every texture as file.RTHBak #
def backup(t_list):
    if PRINT_INFO == True:
        print("[INFO]: Doing backup ...")
    count = 0
    cnt_path = list()
    err = 0
    err_path = list()

    p_root, p_bar = progress_bar("Backup")
    for file in t_list:
        if (count+err)%60 == 0:
            p_bar = update_bar(p_bar, count+err, len(t_list))
        try:
            copyfile(file, f"{file}.RTHBak")
            count += 1
            cnt_path.append(file)
        except Exception as e:
            err += 1
            err_path.append(f"{file}\t{e}")
    if PRINT_INFO == True:
        print(f"[INFO]: Finished Backing up {count}/{len(t_list)} files")
        print(f"[INFO]: Couldn't backup {err} files")
    p_root.destroy()
    return [count, err, cnt_path, err_path]


#=======================================================#
# Copy texture files.RTHBak back to normal texture file #
def restore(t_list):
    if PRINT_INFO == True:
        print("[INFO]: Restoring from backup ...")
    restore = 0
    res_path = list()
    err = 0
    err_path = list()
    p_root, p_bar = progress_bar("Restoring")
    for file in t_list:
        if (restore+err)%60 == 0:
            p_bar = update_bar(p_bar, restore+err, len(t_list))
        try:
            copyfile(f"{file}.RTHBak", file)
            restore += 1
        except Exception as e:
            err += 1
            err_path.append(f"{file}\t{e}")
    if PRINT_INFO == True:
        print(f"[INFO]: Restored {restore}/{len(t_list)} files")
        print(f"[INFO]: Couldn't restore {err} files")
    p_root.destroy()
    return [restore, err, res_path, err_path]


#=================================#
# Delete all texture files.RTHBak #
def delete(t_list):
    if PRINT_INFO == True:
        print("[INFO]: Deleting backup ...")
    delete = 0
    del_path = list()
    err = 0
    err_path = list()
    p_root, p_bar = progress_bar("Deleting")
    for file in t_list:
        if (delete+err)%60 == 0:
            p_bar = update_bar(p_bar, delete+err, len(t_list))
        try:
            os.remove(f"{file}.RTHBak")
            delete += 1
        except Exception as e:
            err += 1
            err_path.append(f"{file}\t{e}")
    if PRINT_INFO == True:
        print(f"[INFO]: Deleted backup: {delete}/{len(t_list)} files")
        print(f"[INFO]: Couldn't delete {err} files")
    p_root.destroy()
    return [delete, err, del_path, err_path]


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


def progress_bar(title):
    p_root = Tk()
    p_root.geometry('640x50'), p_root.title(title)
    p_bar = Progressbar(p_root, orient = 'horizontal', length = 640, mode = 'determinate')
    p_bar.pack(pady = 10), p_root.update(), p_root.protocol("WM_DELETE_WINDOW", 'disable_event')
    return p_root, p_bar


def update_bar(p_bar, i, n):
    p_bar['value'] = int(i / n * 100)
    p_bar.update()
    return p_bar


def submit_report(reports, t_list, opcode):
    cnt = reports[0]
    err = reports[1]
    cnt_path = "\n".join(reports[2])
    err_path = "\n".join(reports[3])

    dt = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    short_msg = f"Finished {BAK_CODE_DICT[opcode].split('.')[0]} {cnt}/{len(t_list)} files\n"\
                f"{err} files spitted out error\n"
    info_msg =  f"For more infomation, check out BAKEDIT_{dt}.log"

    long_msg =  f"{BAK_CODE_DICT[opcode].split('.')[0]} successfully on: \n"+\
                f"{cnt_path}".replace(r"\\", "/") + \
                 "\n\n\n" + ("-" * 128) + "\n\n\n" + \
                 "Caught error on files: \n"+\
                f"{err_path}".replace(r"\\", "/")
    try:
        file = open(f"BAKEDIT_{dt}.log", 'w')
        file.write(short_msg + long_msg)
        file.close()
        messagebox.showinfo("Report", short_msg + info_msg)
    except Exception as e:
        messagebox.showinfo("Report", short_msg + str(e))


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
        reports = confirmation(t_list, opcode)
        if reports is not None:
            submit_report(reports, t_list, opcode)



if __name__ == "__main__":
    print("Run this script from \"Rimworld Texture Helper.py\" instead")


