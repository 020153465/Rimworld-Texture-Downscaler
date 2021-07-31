# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 13:10:27 2021

@author: Saito8546
"""
#####################
# Importing Library #
#####################
import os
import multiprocessing
import datetime

from math import sqrt
from PIL import Image, UnidentifiedImageError
from tkinter import Tk, simpledialog, Entry, Label, messagebox, Button, TclError
from time import sleep
###################
# GLOBAL VARIABLE #
###################
PRINT_INFO = True # Editable from the main file, not here #
PROCESSES = os.cpu_count()
PIXEL_THRESHOLD = None


"""_________________
  /                /
 / TEXTURE EDITOR /
/________________/"""


#====================================================#
# Prompt OPCODE for Function and UI, return int code #
def get_opcode():
    #global PRINT_INFO
    if PRINT_INFO:
        print("[INFO]: Getting Texture operational code")

    try:
        mode = simpledialog.\
            askinteger(title="Texture editor menu",
                      prompt="Input operational code for Texture Editor:\n"
                             "[1 = Texture statistic by threshold pixel area)] - "
                             "Calculate big/small texture files your Mods folder have\n"
                             "[2 = Resize texture down by pixel area threshold] - "
                             "Revert texture back to last backup state\n"
                             "[3 = Color compression menu] - "
                             "Not yet implemented\n"
                             "[Anything else = Return to main menu]\n" +
                             "-" * 128 + "\n"
                             "You should backup your Mods folder yourself or "
                             "with this script before doing any of this")
        if mode is None:
            return -1
        if mode >= 1 and mode <= 3:
            return mode

    # Something went wrong section #
    # Expected exception #
    except (ValueError, TypeError) as e:
        messagebox.showinfo("INFO",
                           f"OPCODE: {mode}\n"
                           f"{e}\n"
                            "Return to main menu !")
    # WTH happened exception #
    except Exception as e:
        messagebox.showerror("ERROR",
                            f"OPCODE: Woah wth just happened ?\n"
                            f"{e}\n"
                             "Return to main menu !")
    return -1


#==========================#
# HOLY BIG MESS OF BANDAGE #===============================#
# Prompt 2 integger numbers, multiply into PIXEL_THRESHOLD #
def update_pixel_threshold():
    p_menu = Tk()
    p_menu.title("Enter pixel area threshold")
    p_menu.resizable(False, False)
    Label(p_menu, text="Width").grid(row=0, sticky='W')
    e1 = Entry(p_menu)
    e1.grid(row=0, column=1)

    Label(p_menu, text="Height").grid(row=1, sticky='W')
    e2 = Entry(p_menu)
    e2.grid(row=1, column=1)

    Label(p_menu, text="Input picture size threshold\n"
          "(Program will use pixel area (width * height) as Threshold"
          ).grid(row=3, sticky='W')
    x = lambda w, h: parse_pixel_threshold(w, h)
    y = lambda: p_menu.destroy()

    b1 = Button(p_menu, text="Confirm", command=lambda: x(e1.get(), e2.get()))
    b1.grid(row=2, column=1, sticky='W')
    b2 = Button(p_menu, text="Cancel", command= lambda: y())
    b2.grid(row=2, column=1, sticky='E')

    # I have no idea what i was doing here #
    while(PIXEL_THRESHOLD is None):
        try:
            p_menu.update()
            sleep(0.0167) # 60 FPS update
        except TclError:
            if PRINT_INFO:
                print("INFO: Cancelled pixel threshold update")
            break

    if PIXEL_THRESHOLD is not None:
        p_menu.destroy()

#==========================#
# HOLY BIG MESS OF BANDAGE #============================#
# Get and parse result from Entry boxes multiply number #
def parse_pixel_threshold(w, h):
    global PIXEL_THRESHOLD
    while PIXEL_THRESHOLD is None:
        try:
            # I have no idea what i was doing here #
            val = (int)(w) * (int)(h)
            PIXEL_THRESHOLD = val
            break
        except Exception:
            if PRINT_INFO == True:
                print(f"ERROR: Both {w} and {h} aren't Integer number")
            break


def count_texture_exceed_threshold(t_list, PIXEL_THRESHOLD, report):
    count = 0
    count_list = list()
    err = 0
    err_list = list()

    for file in t_list:
        f_size = os.stat(file).st_size / 1048576 # Get Megabyte
        try:
            img = Image.open(file)
            w, h = img.size
            if w * h > PIXEL_THRESHOLD:
                count += 1
                count_list.append(f"({w}x{h})\t"
                                  f"{round(f_size, 2)} MB\t"
                                  f"{file}\n")
        except UnidentifiedImageError as e:
            err += 1
            err_list.append(f"{round(f_size, 2)} MB\t"
                            f"{file}\t"
                            f"{e}\n")
    report.append([count, err, count_list, err_list])


def submit_report(reports, t_list):
    global PIXEL_THRESHOLD
    cnt = 0
    err = 0
    cnt_path = ""
    err_path = ""
    c_stripped = 0
    for report in reports:
        cnt += report[0]
        err += report[1]
        for path in report[2]:
            cnt_path += path
        for path in report[3]:
            err_path += path
    dt = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    short_msg = f"Operated on {cnt}/{len(t_list)} texture files that exceeded {PIXEL_THRESHOLD} pixel area\n" \
                f"{err} texture files were skipped\n"
    info_msg =  f"for more infomation, check out {dt}.log"

    long_msg =  f"Texture files exceeded {PIXEL_THRESHOLD} pixel area: \n" +\
                f"{cnt_path}".replace(r"\\", "/") + \
                 "\n\n\n" + ("-" * 128) + "\n\n\n" + \
                f"Texture files were skipped: \n"+\
                f"{err_path}".replace(r"\\", "/")
    try:
        file = open(f"{dt}.log", 'w')
        file.write(short_msg + long_msg)
        file.close()
        messagebox.showinfo("Report", short_msg + info_msg)
    except Exception as e:
        messagebox.showinfo("Report", short_msg + str(e))


def get_resize_mode(t_list):
    if PRINT_INFO:
        print("[INFO]: Getting resize operational code")
    try:
        mode = simpledialog.\
            askinteger(
                title="Resize menu",
                prompt="Choose resizer type: \n"
                        "[1 = Resize texture down by percentage] - "
                        "(Find out how much big/small texture files you have)\n"
                        "[2 = Resize texture down by pixel area threshold] - "
                        "(Revert texture back to last backup state)\n"
                        "[Anything else = Return to main menu]\n" +
                        "-" * 128 + "\n"
                        "You should backup your Mods folder yourself or "
                        "with this script before doing any of this")
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
                            "Return to Texture !")
    # WTH happened exception #
    except Exception as e:
        messagebox.showerror("ERROR",
                            f"OPCODE: Woah wth just happened ?\n"
                            f"{e}\n"
                             "Return to main menu !")
    return -1


def resize_with_pixel_area(t_list, p_area, report):
    count, err, count_list, err_list = 0, 0, list(), list()

    for file in t_list:
        try:
            f_name = "/".join(file.split("\\")[:-1])
            f_ext = file.split("\\")[-1].split(".")[-1]
            f_size = os.stat(file).st_size / 1048576 # Get Megabyte
            img = Image.open(file)
            w, h = img.size

            old_p_area = w * h
            ratio = sqrt(p_area) / sqrt(old_p_area)
            if ratio >= 1:
                continue

            new_w, new_h = int(w * ratio), int(h * ratio)
            if new_w > 0 and new_h > 0:
                img = img.resize((new_w, new_h), resample=Image.LANCZOS, reducing_gap=Image.ANTIALIAS)
                img.save(f"{f_name}_new.{f_ext}", optimize=True, quality=60)
                delta_size = f_size - os.stat(f"{f_name}_new.{f_ext}").st_size / 1048576 # Get Megabyte
                if delta_size > 0:
                    os.remove(file)
                    os.rename(f"{f_name}_new.{f_ext}", file)
                else:
                    class NewFileBiggerThanOldFile(Exception):
                        pass
                    raise NewFileBiggerThanOldFile("Is already well optimized")
                count += 1
                count_list.append(f"({w}x{h}) -> ({new_w}x{new_h})\t"
                                  f"Stripped {round(delta_size, 4)} MB\t"
                                  f"{file}\n")
        except Exception as e:
            err += 1
            err_list.append(f"{round(f_size, 4)} MB\t"
                            f"{file}\t"
                            f"{e}\n")
        img.close()
    report.append([count, err, count_list, err_list])


"""_____________________
  /                    /
 / MULTICORE SUPPORT  /
/____________________/"""
#=========================================#
# Multicore support for some job function #====================#
# Just split big list into small list and feed it into workers #
def mp_job_driver(job, item_list):
    global PIXEL_THRESHOLD
    if PRINT_INFO:
        print("[INFO]: Starting multicore support for the job.")

    foreman = []
    sub_length = len(item_list) // PROCESSES
    report = multiprocessing.Manager().list()

    if PRINT_INFO:
        print(f"[INFO]: Submitting job: ")
    for i in range(0, PROCESSES):
        # Sublist index
        lb = i * sub_length # lowerbound = worker_index * sub length  #
        ub = (i+1) % (PROCESSES) * sub_length - 1 # upperbound is next lower bound - 1 or -1
        if PRINT_INFO:
            print(f"\tWorker[{i}] - {job.__name__} - items[{lb} -> {ub}]")
        # Supply sub lists into the right function #
            worker = multiprocessing.Process(target=job, args=([item_list[lb:ub], PIXEL_THRESHOLD, report]))
            worker.start()
            foreman.append(worker)

    # # Collecting results #
    if PRINT_INFO:
         print("[INFO]: Workers reporting in: ")
    # Contain sub results into list to send to the right parser #
    for i in range(0, PROCESSES):
         foreman[i].join()
         if PRINT_INFO:
             print(f"\tWorker{[i]} - Reported in")

    return report


def main(t_list, info):
    global PIXEL_THRESHOLD, PRINT_INFO
    PRINT_INFO = info
    # UI Loop #
    while t_list is not None:
        ###################
        # UI & Job Driver #
        ###################
        opcode = get_opcode()
        if opcode == -1:
            break

        ###############################################
        # Update pixel area threshold every operation #
        ###############################################
        if PRINT_INFO:
            print(f"[INFO]: Prompting for pixel area threshold")
        update_pixel_threshold()
        if PIXEL_THRESHOLD is None:
            continue

        ##################################################
        # Count texture number with pixel area threshold #
        ##################################################
        if opcode == 1:
            if PRINT_INFO:
                print(f"[INFO]: Counting texture with pixel area > {PIXEL_THRESHOLD}")
            reports = mp_job_driver(count_texture_exceed_threshold, t_list)
            submit_report(reports, t_list)

        #################################################
        # Resize texture exceeding pixel area threshold #
        #################################################
        if opcode == 2:
            reports = mp_job_driver(resize_with_pixel_area, t_list)
            submit_report(reports, t_list)
            t_list = None

        PIXEL_THRESHOLD = None

    return t_list