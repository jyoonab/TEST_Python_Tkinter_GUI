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


"""class Main_Frame(Frame):
    def __init__(self, ws):
        Frame.__init__(self, ws, height=300, width=300, bg="#006699")
        self.ws = ws
        self.widgets()

    def widgets(self):
        self.text = Label(self, text="This label is on the frame ")
        self.text.grid(row=0, column=0, padx=10, pady=20) # margins"""

class Main_Form(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("app")
        self.geometry("450x600")
        #self.resizable(0, 0)


        # logo design
        logo = Image.open('./Resources/Images/logo.png')
        logo = logo.resize((60, 18), Image.ANTIALIAS)
        logo_photo: object = ImageTk.PhotoImage(logo)
        self.logo_image = Label(self, image=logo_photo, justify=RIGHT)
        self.logo_image.image = logo_photo
        self.logo_image.grid(column=0, row=0, sticky="w", padx=(20, 10), pady=(20, 10))

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

        # profile design
        profile = Image.open('./Resources/Images/profile.png')
        profile = profile.resize((40, 40), Image.ANTIALIAS)
        profile_photo: object = ImageTk.PhotoImage(profile)
        self.profile_image = Label(self, image=profile_photo)
        self.profile_image.image = profile_photo
        self.profile_image.grid(column=0, row=1, sticky="e", padx=(20, 20), pady=(10, 10))

        self.profile_id_label: object = tk.Label(self, text="test@gmail.com",
                                                 font=tkFont.Font(family="Roboto", size=12))
        self.profile_id_label.grid(column=1, row=1, sticky="w", padx=(0, 0), pady=(10, 10))

        # Input device design
        self.microphone_label: object = tk.Label(self,
                                                 text="microphone",
                                                 font=tkFont.Font(family="Roboto", size=12))
        self.microphone_label.grid(column=0, row=2, sticky="w", padx=(20, 10), pady=(40, 0))

        microphone = Image.open('./Resources/Images/microphone.png')
        microphone = microphone.resize((40, 40), Image.ANTIALIAS)
        microphone_photo: object = ImageTk.PhotoImage(microphone)
        self.microphone_image = Label(self, image=microphone_photo)
        self.microphone_image.image = microphone_photo
        self.microphone_image.grid(column=0, row=3, sticky="e", padx=(20, 20), pady=(10, 10))

        self.input_device_dict, self.output_device_dict = Function.get_sound_devices()

        self.input_device_combo: object = ttk.Combobox(self, state="readonly", width=25,
                                                       font=tkFont.Font(family="나눔고딕", size=11),
                                                       values=list(self.input_device_dict.keys()))
        self.input_device_combo.grid(column=1, row=3, sticky="w", padx=(0, 0), pady=(10, 10))
        self.input_device_combo.current(0)

        # Output device design
        self.speaker_label: object = tk.Label(self,
                                              text="speaker",
                                              font=tkFont.Font(family="Roboto", size=12))
        self.speaker_label.grid(column=0, row=4, sticky="w", padx=(20, 10), pady=(40, 0))

        speaker = Image.open('./Resources/Images/speaker.png')
        speaker = speaker.resize((40, 40), Image.ANTIALIAS)
        speaker_photo: object = ImageTk.PhotoImage(speaker)
        self.speaker_image = Label(self, image=speaker_photo)
        self.speaker_image.image = speaker_photo
        self.speaker_image.grid(column=0, row=5, sticky="e", padx=(20, 20), pady=(10, 10))

        self.output_device_combo: object = ttk.Combobox(self, state="readonly", width=25,
                                                        font=tkFont.Font(family="나눔고딕", size=11),
                                                        values=list(self.output_device_dict.keys()))
        self.output_device_combo.grid(column=1, row=5, sticky="w", padx=(0, 0), pady=(10, 10))
        self.output_device_combo.current(0)

        # Start button design
        self.start_button: object = tk.Button(self, overrelief="solid", width=10, height=2,
                                              repeatdelay=1000, repeatinterval=100,
                                              text="start",
                                              font=tkFont.Font(family="Roboto", size=12),
                                              command=lambda: Event.start_button_clicked())
        self.start_button.grid(column=1, row=6, sticky="e", padx=(20, 10), pady=(40, 10))

        # Serial Design
        self.serial_label: object = tk.Label(self, text="You have 120 mins", bg='gray',
                                             font=tkFont.Font(family="Roboto", size=12))
        self.serial_label.grid(column=0, row=7, sticky="w", padx=(20, 0), pady=(40, 0), columnspan=2)


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


if __name__ == '__main__':
    main_form = Main_Form()
    main_form.protocol("WM_DELETE_WINDOW", Event.main_form_closing)
    main_form.mainloop()  # execute GUI
