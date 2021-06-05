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

class Header_Frame(Frame):
    def __init__(self, ws):
        Frame.__init__(self, ws, relief="solid", bd=1)
        self.ws = ws
        self.widgets()

    def widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Main logo design
        main_logo_height = 100
        main_logo = Image.open('./Resources/Images/mainLogo.png')
        main_logo_width = Function.get_width_size_with_fixed_aspect_ratio(main_logo_height, main_logo.size[0], main_logo.size[1])
        main_logo = main_logo.resize((main_logo_height, main_logo_width), Image.ANTIALIAS)
        main_logo_photo: object = ImageTk.PhotoImage(main_logo)
        self.main_logo_image = Label(self, image=main_logo_photo, justify=RIGHT)
        self.main_logo_image.image = main_logo_photo
        self.main_logo_image.grid(column=0, row=0, sticky="w", padx=(10, 10), pady=(0, 0))

        # User Icon design
        user_icon_height = 30
        user_icon = Image.open('./Resources/Images/user2.png')
        user_icon_width = Function.get_width_size_with_fixed_aspect_ratio(user_icon_height, user_icon.size[0], user_icon.size[1])
        user_icon = user_icon.resize((user_icon_height, user_icon_width), Image.ANTIALIAS)
        user_icon_photo: object = ImageTk.PhotoImage(user_icon)
        self.user_icon_image = Label(self, image=user_icon_photo, justify=RIGHT)
        self.user_icon_image.image = user_icon_photo
        self.user_icon_image.grid(column=0, row=1, sticky="w", padx=(10, 10), pady=(0, 0))



        # preferences button design
        self.menu_button: object = tk.Menubutton(self, relief="raised", width=10, height=2,
                                                 text="menu",
                                                 font=tkFont.Font(family="Roboto", size=12))
        self.menu_button.grid(column=1, row=0, sticky="e", padx=(20, 10), pady=(20, 10))

        self.menu = tk.Menu(self.menu_button, tearoff=0, font=tkFont.Font(family="Roboto", size=12))
        self.menu.add_command(label="About")
        self.menu.add_command(label="Preferences", command=Event.preferences_menu_clicked)
        self.menu.add_command(label="Check for update")
        self.menu.add_separator()
        self.menu.add_command(label="Report & Support")
        self.menu.add_command(label="Contact us")
        self.menu.add_separator()
        self.menu.add_command(label="Sign out")
        self.menu.add_command(label="Quit")

        self.menu_button["menu"] = self.menu

class Footer_Frame(Frame):
    def __init__(self, ws):
        Frame.__init__(self, ws, relief="solid", bd=0)
        self.ws = ws
        self.widgets()

    def widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # logo design
        time_left_label = tk.Label(self, text="Time Left: 24 HR")
        time_left_label.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), sticky='w')

        # preferences button design
        start_button = tk.Button(self, overrelief="solid", width=15, text="Buy License", repeatdelay=1000, repeatinterval=100)
        start_button.grid(column=1, row=0, padx=(10, 10), pady=(10, 10), sticky='e')

class Input_Device_Frame(Frame):
    def __init__(self, ws):
        Frame.__init__(self, ws, relief="solid", bd=0)
        self.ws = ws
        self.widgets()

    def widgets(self):
        # Input device design
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)

        self.microphone_label: object = tk.Label(self,
                                                 text="microphone",
                                                 font=tkFont.Font(family="Roboto", size=12))
        self.microphone_label.grid(column=0, row=0, sticky="w", padx=(20, 10), pady=(40, 0))

        microphone = Image.open('./Resources/Images/microphone.png')
        microphone = microphone.resize((100, 100), Image.ANTIALIAS)
        microphone_photo: object = ImageTk.PhotoImage(microphone)
        self.microphone_image = Label(self, image=microphone_photo)
        self.microphone_image.image = microphone_photo
        self.microphone_image.grid(column=0, row=1, sticky="w", padx=(20, 20), pady=(10, 10))

        self.input_device_dict, self.output_device_dict = Function.get_sound_devices()

        self.input_device_combo: object = ttk.Combobox(self, state="readonly", width=25,
                                                       font=tkFont.Font(family="나눔고딕", size=11),
                                                       values=list(self.input_device_dict.keys()))
        self.input_device_combo.grid(column=1, row=1, sticky="e", padx=(10, 10), pady=(10, 10))
        self.input_device_combo.current(0)

class Output_Device_Frame(Frame):
    def __init__(self, ws):
        Frame.__init__(self, ws, relief="solid", bd=0)
        self.ws = ws
        self.widgets()

    def widgets(self):
        # Output device design
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)

        self.speaker_label: object = tk.Label(self,
                                              text="speaker",
                                              font=tkFont.Font(family="Roboto", size=12))
        self.speaker_label.grid(column=0, row=0, sticky="w", padx=(20, 10), pady=(40, 0))

        speaker = Image.open('./Resources/Images/speaker.png')
        speaker = speaker.resize((100, 100), Image.ANTIALIAS)
        speaker_photo: object = ImageTk.PhotoImage(speaker)
        self.speaker_image = Label(self, image=speaker_photo)
        self.speaker_image.image = speaker_photo
        self.speaker_image.grid(column=0, row=1, sticky="w", padx=(20, 20), pady=(10, 10))

        self.input_device_dict, self.output_device_dict = Function.get_sound_devices()

        self.output_device_combo: object = ttk.Combobox(self, state="readonly", width=25,
                                                        font=tkFont.Font(family="나눔고딕", size=11),
                                                        values=list(self.output_device_dict.keys()))
        self.output_device_combo.grid(column=1, row=1, sticky="e", padx=(10, 10), pady=(10, 10))
        self.output_device_combo.current(0)

class Main_Form(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("app")
        self.geometry("450x550")
        #self.resizable(0, 0)

        # Make Window Draggable
        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind("<ButtonRelease-1>", self.StopMove)
        self.bind("<B1-Motion>", self.OnMotion)

        # Header Frame
        self.header_frame = Header_Frame(self)
        self.header_frame.pack(fill="both", expand=False)

        # Input Device Frame
        self.input_device_frame = Input_Device_Frame(self)
        self.input_device_frame.pack(fill="both", expand=True)

        # Output Device Frame
        self.output_device_frame = Output_Device_Frame(self)
        self.output_device_frame.pack(fill="both", expand=True)

        # Footer Frame
        self.footer_frame = Footer_Frame(self)
        self.footer_frame.pack(fill="both", expand=False)

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
    def start_button_clicked():
        # get preference setting data
        preferences_data = Function.get_preferences_pack('./Resources/Settings/preferences.json')
        aec_mode: bool = eval(preferences_data['advanced']['aec_mode'])
        high_performance_mode: bool = eval(preferences_data['advanced']['high_performance_mode'])

        # get service_type_index
        # "high performance mode": 0, "acoustic echo cancellation mode": 1, "acoustic noise reduction mode": 2
        if high_performance_mode is True:
            service_type_index: int = int(0)
        elif aec_mode is True and high_performance_mode is False:
            service_type_index: int = int(1)
        else:
            service_type_index: int = int(2)

        ai_process_count: int = Function.count_ai_process()
        print(ai_process_count)

        if main_form.start_button['text'] == 'Start' and ai_process_count == int(0):
            # Start Event
            if service_type_index == int(0):  # 0: premium service
                message_box: str = messagebox.askquestion('test',
                                                          'Premium service is recommended for high-performance devices.\n\n'
                                                          'Are you sure you want to continue?', icon='warning')
                if message_box == str('no'):
                    return

            input_device_index: int = main_form.input_device_dict[main_form.input_device_combo.get()]
            output_device_index: int = main_form.output_device_dict[main_form.output_device_combo.get()]

            args = 'test_ai.exe --input {0} --output {1} --service {2}' \
                .format(input_device_index, output_device_index, service_type_index)
            print(args)

            try:
                subprocess.Popen(args, shell=True)
            except Exception as ex:
                messagebox.showinfo("Sorry :<", f'Error Occurred: {str(ex)}')

            main_form.start_button['text'] = str('Stop')

        elif main_form.start_button['text'] == str('Stop') and ai_process_count != int(0):
            # Stop Event
            message_box: str = messagebox.askquestion('test',
                                                      'Are you sure want to stop the test service', icon='warning')
            if message_box == str('no'):
                return

            Function.kill_ai_process()
            main_form.start_button['text'] = str('Start')

        else:
            # Exception Event
            if messagebox.askokcancel("Notice", "The process is already running. Are you sure you want to exit?"):
                # Ok Button Click Event
                Function.kill_ai_process()
                main_form.start_button['text'] = str('Start')
            else:
                # Cancel Button Click Event
                messagebox.showinfo("Notice", "Please re-try it after terminating the existing process.")
                return

    @staticmethod
    def preferences_menu_clicked():
        preference_form = Preferences_Form()
        preference_form.activate()

    @staticmethod
    def main_form_closing():
        if messagebox.askokcancel("Notice", "Are you sure to close the window?"):
            main_form.destroy()


class Function:
    @staticmethod
    def count_ai_process():
        process_count: int = int(0)
        for process in psutil.process_iter():
            process_name: str = process.name()
            if process_name == str('test_ai.exe'):
                process_count += int(1)
        return process_count

    @staticmethod
    def kill_ai_process():
        target_process_name: str = str("noiist_ai.exe")
        for process in psutil.process_iter():
            try:
                process_name: str = process.name()
                if process_name == target_process_name:
                    process.kill()
            except Exception as ex:
                messagebox.showinfo("Sorry :<", f'Error Occurred: {str(ex)}')
                continue

    @staticmethod
    def get_sound_devices():
        """ This function get input/output audio device information """
        TARGET_VIRTUAL_DEVICE: str = 'CABLE Input'
        INPUT_EXCEPT_DEVICE_LIST: List[str] = ['CABLE Output', 'Microsoft Sound Mapper - Input',
                                               'Microsoft Sound Mapper - Output', 'Microsoft 사운드 매퍼',
                                               '주 사운드 캡처 드라이버', '주 사운드 드라이버', '라인 입력', 'Output ()', '스테레오 믹스']
        OUTPUT_EXCEPT_DEVICE_LIST: List[str] = ['CABLE Output', 'Microsoft Sound Mapper - Input', 'Microsoft 사운드 매퍼',
                                                'Microsoft Sound Mapper - Output', '스테레오 믹스', 'SPDIF Out',
                                                '주 사운드 캡처 드라이버', '주 사운드 드라이버', '라인 입력', 'Output ()', '마이크']

        input_device_dict: Dict[str, int] = dict()
        output_device_dict: Dict[str, int] = dict()

        device_list: object = sd.query_devices()

        for index, device in enumerate(device_list):
            if device['default_samplerate'] != 44100.0:  # if not sample rate 44100:
                continue

            if device['hostapi'] != 0:  # if not host api is 0
                continue

            if '(' in device['name']:  # make a device name more beautiful
                device['name'] = device['name'][0:device['name'].index('(')]

            # get input devices
            if device['max_input_channels'] != int(0) and device["max_output_channels"] == int(0):
                if device['name'] in INPUT_EXCEPT_DEVICE_LIST:  # exception based on device name
                    continue

                input_device_dict[device['name']] = index

            # get output devices
            if device['max_input_channels'] == int(0) and device["max_output_channels"] != int(0):
                if device['name'] in OUTPUT_EXCEPT_DEVICE_LIST:  # exception based on device name
                    continue

                if TARGET_VIRTUAL_DEVICE in device['name']:
                    device['name'] = '딥러닝 기반 음향 품질향상 모드'

                output_device_dict[device['name']] = index

        return input_device_dict, output_device_dict

    @staticmethod
    def get_width_size_with_fixed_aspect_ratio(fixed_logo_height, real_height, real_width):
        width_percent = (fixed_logo_height / float(real_height))
        return int((float(real_width) * float(width_percent)))

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
