# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 21:13:18 2021

@author: Saito8546
"""
#####################
# Importing Library #
#####################
import sys, os

from glob import glob
from tkinter import Tk, simpledialog, messagebox, filedialog


###################
# GLOBAL VARIABLE #
###################
PRINT_INFO = True # Editable

# UI Driver Type #
TEX_EDITOR = None
BAK_EDITOR = None

# Make a top-level instance and hide since it is ugly and big. #
ROOT = Tk()
ROOT.withdraw()


"""_____________
  /            /
 / MAIN MENU  /
/____________/"""

#================================#
# Ensure no module files missing #
def check_module():
    red_flag = False
    msg = ""
    if os.path.exists("texture_editor.py"):
        global TEX_EDITOR
        TEX_EDITOR = __import__("texture_editor")
    else:
        msg += "'texture_editor.py' "
        red_flag = True

    if os.path.exists("backup_editor.py"):
        global BAK_EDITOR
        BAK_EDITOR = __import__("backup_editor")
    else:
        red_flag = True
        msg += "'backup_editor.py'"

    if red_flag:
        if PRINT_INFO:
            print(f"[ERROR]: Missing {msg} module(s)\nAborting Script")
        messagebox.showerror("ERROR", f"Missing {msg} module(s)\n"
                                         "ABORTING SCRIPT")
        sys.exit(-1)

#=================================================#
# Prompt OPCODE for Main menu UI, return int code #
def get_opcode():
    if PRINT_INFO:
        print("[INFO]: Getting operational code")

    try:
        mode = simpledialog.\
            askinteger(title="Main menu",
                      prompt="Input operational code:\n"
                             "[1 = Texture Editor]\n"
                             "[2 = Backup Editor] - Very Basic\n"
                             "[Anything else = Exit]\n" +
                             "-" * 48 + "\n"
                             "Much info, many features\n")
        if mode is None:
            return -1
        if mode >= 1 and mode <= 2:
            return mode

    # Something went wrong section #
    # Expected exception #
    except (ValueError, TypeError) as e:
        messagebox.showinfo("INFO",
                           f"OPCODE: {mode}\n"
                           f"{e}\n"
                            "ABORTING SCRIPT !")
    # WTH happened exception #
    except Exception as e:
        messagebox.showerror("ERROR",
                            f"OPCODE: Woah wth just happened ?\n"
                            f"{e}\n"
                             "ABORTING SCRIPT !")
    return -1


#=============================================================#
# Find and read cached mod folder, return string path or None #
def get_cached_mod_folder():
    if os.path.exists("RTH.cache"):
        file = open("RTH.cache", 'r', encoding='utf-8')
        mod_dir = file.readline()
        file.close()

        if mod_dir.split("/")[-1] == "Mods" and \
            os.path.exists(f"{mod_dir}"[:-4] + "UnityPlayer.dll"):
            if PRINT_INFO:
                print("[INFO]: Found cached mod folder path")
            return mod_dir

    # Something went wrong section #
    if PRINT_INFO:
        print("[INFO]: Cached file is Missing or Corrupted")
    return None


#=========================================================================#
# Prompt path to Rimworld's mod folder, return string path or exit script #
def get_mod_folder():
    if PRINT_INFO:
        print("[INFO]: Getting Rimworld's mod folder")

    curr_dir = os.getcwd()
    mod_dir = filedialog.askdirectory(initialdir = curr_dir,\
                                        title="Select Rimworld's mod directory")

    # Check if correct Mods folder #
    if mod_dir.split("/")[-1] == "Mods" and \
        os.path.exists(f"{mod_dir}"[:-4] + "UnityPlayer.dll"):
        messagebox.showinfo("INFO",
                            "Folder you selected: \n"
                           f"{mod_dir}\n"
                           f"Seem to be the correct mod folder.")

        # Save to cache file #
        file = open("RTH.cache", 'w', encoding='utf-8')
        file.write(mod_dir)
        file.close()

        return mod_dir

    # Something went wrong section #
    messagebox.showerror("ERROR",
                         "Folder you selected: \n"
                        f"{mod_dir}\n" \
                         "Doesn't look like Rimworld's mod folder !\n"\
                         "Aborting script.")

    sys.exit(-1)


#============================================================#
# Get list of texture files, return string texture path list #
# if no texture file found, exit script                      #
def get_texture_list(mod_dir):
    if PRINT_INFO:
        print(f"[INFO]: Finding texture files in {mod_dir}")

    # Get all files in mod_dir #
    file_list = glob(f"{mod_dir}/**/*.*", recursive = True)

    texture_list = list()
    exts = ('png', 'jpg', 'jpeg')
    for file in file_list:
        # Is correct file extention #
        if file.split(".")[-1].lower() in exts:
            # Is NOT mod preview picture #
            if file.split("\\")[-2] != "About":
                texture_list.append(rf"{file}")

    if PRINT_INFO:
        t_len = len(texture_list)
        if PRINT_INFO:
            print(f"[INFO]: Found {t_len} texture file(s)")

        # Something went wrong section #
        if t_len == 0:
            print("No texture file found, this doesn't seem right ?")
            messagebox.showerror("ERROR",
                                 "No texture file found ! Empty mod folder ?\n"
                                 "! ABORTING SCRIPT !")
            sys.exit(-1)

    return texture_list


########################
# MAIN - IT DOES STUFF #
########################
def main():
    print("Welcome to Saito8546's Potato Rimworld Texture Helper")
    # Get Rimworld's mod folder #
    mod_dir = get_cached_mod_folder()
    if mod_dir is None:
        mod_dir = get_mod_folder()

    # Initial operational code #
    opcode = 0
    t_list = None

    # UI Loop #
    while opcode != -1:
        #############
        # UI DRIVER #
        #############
        opcode = get_opcode()
        if t_list is None and opcode != -1:
            t_list = get_texture_list(mod_dir)

        ##################
        # TEXTURE EDITOR #
        ##################
        if opcode == 1:
            t_list = TEX_EDITOR.main(t_list, PRINT_INFO)

        ###################
        # BACKUP OPERATOR #
        ###################
        elif opcode == 2:
            BAK_EDITOR.main(t_list, PRINT_INFO)


    if PRINT_INFO:
        print("[INFO]: Closing program ...")
    sys.exit(1)


##########################################
# SAFE MAIN RUNNER - NOTHING TO SEE HERE #
##########################################
if __name__ == "__main__":
    check_module()
    main()