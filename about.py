# Libraries
import sounddevice as sd
from tkinter.ttk import *
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import subprocess
import psutil
import tempfile
import os
import shutil
import time
from typing import List, Union, Dict, Any
import json
from ctypes import windll

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

class Frame:
    def create_main_frame(container):
        frame = ttk.Frame(container, padding=0, relief='flat')

        frame.columnconfigure(0, weight=20)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=40)

        frame.rowconfigure(0, weight=1)

        # Main logo design
        main_logo_photo, main_logo_width, main_logo_height = Function.get_image(150, './Resources/Images/mainLogo.png')
        frame.main_logo_image = Label(frame, image=main_logo_photo)
        frame.main_logo_image.image = main_logo_photo
        frame.main_logo_image.grid(column=0, row=0, sticky="wens", padx=(10, 0), pady=(10, 10))

        # Separator
        input_status_label = tk.Label(frame, text="|", font='Helvetical 60')
        input_status_label.grid(column=1, row=0, padx=(0, 10), pady=(10, 10), sticky="wens")

        ################## right frame ##################
        sub_frame_right = ttk.Frame(frame, padding=0, relief='flat') # for mic icon & input_device_combo
        sub_frame_right.grid(column=2, row=0, sticky=W+E, padx=(0, 5), pady=(0, 0))

        sub_frame_right.rowconfigure(0, weight=1)
        sub_frame_right.rowconfigure(1, weight=1)
        sub_frame_right.rowconfigure(2, weight=1)
        sub_frame_right.rowconfigure(3, weight=1)


        product_full_name_label = tk.Label(sub_frame_right, text="Windows OS용 Acoustic Noise Cancellation", font='Helvetical 10 bold')
        product_full_name_label.grid(column=0, row=0, padx=(3, 0), pady=(10, 2), sticky="w")


        version_label = tk.Label(sub_frame_right, text="버전 1.0.0 (빌드 1)", font='Helvetical 10')
        version_label.grid(column=0, row=1, padx=(3, 0), pady=(2, 2), sticky="w")


        summary_label = tk.Message(sub_frame_right, width= 200, text="본 프로그램은 존나 쩝니다. 개쩝니다. 본 프로그램은 존나 쩝니다. 개쩝니다. 본 프로그램은 존나 쩝니다. 개쩝니다.", font='Helvetical 10')
        summary_label.grid(column=0, row=2, padx=(0, 0), pady=(2, 2), sticky="w")


        copy_rights_label = tk.Label(sub_frame_right, text="@ 2021 All Rights Reserved", font='Helvetical 10')
        copy_rights_label.grid(column=0, row=3, padx=(3, 0), pady=(2, 10), sticky="w")

        frame.mic_button: object = tk.Button(frame, relief="flat", text="Terms and Conditions", bg="#cdd1ce")
        frame.mic_button.grid(column=2, row=1, sticky="e", padx=(10, 10), pady=(10, 10))

        return frame

    def create_footer_frame(container):
        frame = ttk.Frame(container, padding=0, relief='flat')
        frame.columnconfigure(1, weight=1)

        frame.mic_button: object = tk.Button(frame, relief="flat", text="Terms and Conditions", bg="#cdd1ce", font='Helvetical 10')
        frame.mic_button.grid(column=1, row=0, sticky="e", padx=(10, 10), pady=(10, 10))

        return frame

class Main_Form(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("app")
        self.geometry("550x200")
        self.resizable(0, 0)

        # Make Window Draggable
        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind("<ButtonRelease-1>", self.StopMove)
        self.bind("<B1-Motion>", self.OnMotion)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)

        # Main Frame
        header_frame = Frame.create_main_frame(self)
        header_frame.grid(column=0, row=0,  padx=(5, 5), pady=(5, 5), sticky=W+E+N+S)


    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))


class Event:
    @staticmethod
    def main_form_closing():
        if messagebox.askokcancel("Notice", "Are you sure to close the window?"):
            main_form.destroy()


class Function:
    @staticmethod
    def get_height_size_with_fixed_aspect_ratio(fixed_logo_width, real_width, real_height):
        width_percent = (fixed_logo_width / float(real_width))
        return int((float(real_height) * float(width_percent)))

    @staticmethod
    def get_image(height, path):
        main_logo_width = height
        main_logo = Image.open(path)
        main_logo_height = Function.get_height_size_with_fixed_aspect_ratio(main_logo_width, main_logo.size[0], main_logo.size[1])
        main_logo = main_logo.resize((main_logo_width, main_logo_height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(main_logo), main_logo_width, main_logo_height # returns image, width, height

    @staticmethod
    def set_appwindow(root): # make program appear on windows taskbar
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())


if __name__ == '__main__':
    main_form = Main_Form()
    main_form.protocol("WM_DELETE_WINDOW", Event.main_form_closing)

    main_form.overrideredirect(1)    #eliminate the titlebar
    main_form.after(10, lambda: Function.set_appwindow(main_form)) # make program appear on windows taskbar

    main_form.mainloop()  # execute GUI
