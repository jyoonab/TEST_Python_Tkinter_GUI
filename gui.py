# Libraries
import sounddevice as sd
from tkinter.ttk import *
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

class Frame:
    def create_header_frame(container):
        frame = ttk.Frame(container, padding=0, relief='flat')

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Main logo design
        main_logo_photo, main_logo_width, main_logo_height = Function.get_image(150, './Resources/Images/mainLogo.png')
        frame.main_logo_image = Label(frame, image=main_logo_photo, justify=RIGHT)
        frame.main_logo_image.image = main_logo_photo
        frame.main_logo_image.grid(column=0, row=0, sticky="w", padx=(0, 10), pady=(0, 0))

        # preferences button design
        menu_icon_photo, menu_icon_width, menu_icon_height = Function.get_image(30, './Resources/Images/menu.png')
        frame.menu_icon_image = Label(frame, image=menu_icon_photo, justify=RIGHT)
        frame.menu_icon_image.image = menu_icon_photo

        frame.menu_button: object = tk.Menubutton(frame, relief="flat", width=menu_icon_width, height=menu_icon_height,
                                                 image=menu_icon_photo)
        frame.menu_button.grid(column=1, row=0, sticky="e", padx=(10, 10), pady=(0, 0))

        frame.menu = tk.Menu(frame.menu_button, tearoff=0, font=tkFont.Font(family="Roboto", size=12))
        frame.menu.add_command(label="About")
        frame.menu.add_command(label="Preferences", command=Event.preferences_menu_clicked)
        frame.menu.add_command(label="Check for update")
        frame.menu.add_separator()
        frame.menu.add_command(label="Report & Support")
        frame.menu.add_command(label="Contact us")
        frame.menu.add_separator()
        frame.menu.add_command(label="Sign out")
        frame.menu.add_command(label="Quit")

        frame.menu_button["menu"] = frame.menu

        return frame

    def create_statue_frame(container):
        frame = ttk.Frame(container, padding=0, relief='flat')

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=20)
        frame.columnconfigure(2, weight=20)

        user_photo, user_width, user_height = Function.get_image(20, './Resources/Images/user2.png')
        frame.user_photo_image = Label(frame, image=user_photo, justify=RIGHT)
        frame.user_photo_image.image = user_photo
        frame.user_photo_image.grid(column=0, row=0, sticky="w", padx=(20, 0), pady=(0, 10))

        email_label = tk.Label(frame, text="jyoona12345@gmail.com")
        email_label.grid(column=1, row=0, padx=(0, 0), pady=(0, 10), sticky='w')

        status_label = tk.Label(frame, text="Free")
        status_label.grid(column=2, row=0, padx=(10, 10), pady=(0, 10), sticky='e')

        return frame

    def create_input_frame(container):
        style = ttk.Style()
        style.configure("BW.TLabel", background="white")

        frame = ttk.Frame(container, padding=0, relief='groove', style="BW.TLabel")

        ################## label frame ##################
        sub_frame_label = ttk.Frame(frame, padding=0, relief='flat', style="BW.TLabel") # for mic icon & input_device_combo
        sub_frame_label.columnconfigure(0, weight=1)
        sub_frame_label.columnconfigure(1, weight=20)
        sub_frame_label.grid(column=0, row=0, sticky=W+E, padx=(5, 0), pady=(1, 0))

        # label
        mic_label = tk.Label(sub_frame_label, text="Microphone", bg="white", font='Helvetical 18 bold')
        mic_label.grid(column=0, row=0, padx=(20, 10), pady=(10, 0), sticky='w')

        input_status_label = tk.Label(sub_frame_label, text="Not Used", bg="white")
        input_status_label.grid(column=1, row=0, padx=(10, 10), pady=(10, 0), sticky='e')

        input_status_label = tk.Label(sub_frame_label, text="Test Noise Cancellation", bg="white", font='Helvetical 12 bold')
        input_status_label.grid(column=0, row=1, padx=(20, 10), pady=(0, 10), sticky='w')

        ################## input frame ##################
        sub_frame_input = ttk.Frame(frame, padding=0, relief='flat', style="BW.TLabel") # for mic icon & input_device_combo
        sub_frame_input.columnconfigure(0, weight=1)
        sub_frame_input.columnconfigure(1, weight=10)
        sub_frame_input.grid(column=0, row=1, sticky=W+E, padx=(5, 0), pady=(0, 0))

        # mic icon image
        mic_icon_photo, mic_icon_width, mic_icon_height = Function.get_image(30, './Resources/Images/mic.png')
        frame.mic_icon_image = Label(sub_frame_input, image=mic_icon_photo, justify=RIGHT)
        frame.mic_icon_image.image = mic_icon_photo
        frame.mic_button: object = tk.Button(sub_frame_input, relief="groove", width=mic_icon_width, height=mic_icon_height, image=mic_icon_photo)
        frame.mic_button.grid(column=0, row=0, sticky="w", padx=(15, 0), pady=(0, 0))

        # input combo
        frame.input_device_dict, frame.output_device_dict = Function.get_sound_devices()
        frame.input_device_combo: object = ttk.Combobox(sub_frame_input, state="readonly", width=40,
                                                       values=list(frame.input_device_dict.keys()))
        frame.input_device_combo.grid(column=1, row=0, sticky="e", padx=(0, 0), pady=(0, 0))
        frame.input_device_combo.current(0)

        ################## noise cancellation selector frame ##################
        sub_frame_noise_cancellation_selector = ttk.Frame(frame, padding=0, relief='flat', style="BW.TLabel") # for mic icon & input_device_combo
        sub_frame_noise_cancellation_selector.columnconfigure(0, weight=5)
        sub_frame_noise_cancellation_selector.columnconfigure(1, weight=1)
        sub_frame_noise_cancellation_selector.grid(column=0, row=2, sticky=W+E, padx=(5, 0), pady=(0, 5))
        remove_noise_label = tk.Label(sub_frame_noise_cancellation_selector, text="Remove Noise", bg="white")
        remove_noise_label.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), sticky='e')
        remove_noise_selector = tk.Label(sub_frame_noise_cancellation_selector, text="Foo", bg="white")
        remove_noise_selector.grid(column=1, row=0, padx=(10, 10), pady=(10, 10), sticky='e')

        return frame

    def create_output_frame(container):
        style = ttk.Style()
        style.configure("BW.TLabel", background="white")

        frame = ttk.Frame(container, padding=0, relief='groove', style="BW.TLabel")

        ################## label frame ##################
        sub_frame_label = ttk.Frame(frame, padding=0, relief='flat', style="BW.TLabel") # for mic icon & input_device_combo
        sub_frame_label.columnconfigure(0, weight=1)
        sub_frame_label.columnconfigure(1, weight=20)
        sub_frame_label.grid(column=0, row=0, sticky=W+E, padx=(5, 0), pady=(1, 0))

        # label
        mic_label = tk.Label(sub_frame_label, text="Speaker", bg="white", font='Helvetical 18 bold')
        mic_label.grid(column=0, row=0, padx=(20, 10), pady=(10, 20), sticky='w')

        input_status_label = tk.Label(sub_frame_label, text="Not Used", bg="white")
        input_status_label.grid(column=1, row=0, padx=(10, 10), pady=(10, 20), sticky='e')

        ################## input frame ##################
        sub_frame_input = ttk.Frame(frame, padding=0, relief='flat', style="BW.TLabel") # for mic icon & input_device_combo
        sub_frame_input.columnconfigure(0, weight=1)
        sub_frame_input.columnconfigure(1, weight=10)
        sub_frame_input.grid(column=0, row=1, sticky=W+E, padx=(5, 0), pady=(0, 0))

        # mic icon image
        mic_icon_photo, mic_icon_width, mic_icon_height = Function.get_image(30, './Resources/Images/speaker.png')
        frame.mic_icon_image = Label(sub_frame_input, image=mic_icon_photo, justify=RIGHT)
        frame.mic_icon_image.image = mic_icon_photo
        frame.mic_button: object = tk.Button(sub_frame_input, relief="groove", width=mic_icon_width, height=mic_icon_height, image=mic_icon_photo)
        frame.mic_button.grid(column=0, row=0, sticky="w", padx=(15, 0), pady=(0, 0))

        # input combo
        frame.input_device_dict, frame.output_device_dict = Function.get_sound_devices()
        frame.input_device_combo: object = ttk.Combobox(sub_frame_input, state="readonly", width=40,
                                                       values=list(frame.output_device_dict.keys()))
        frame.input_device_combo.grid(column=1, row=0, sticky="e", padx=(0, 0), pady=(0, 0))
        frame.input_device_combo.current(0)

        ################## noise cancellation selector frame ##################
        sub_frame_noise_cancellation_selector = ttk.Frame(frame, padding=0, relief='flat', style="BW.TLabel") # for mic icon & input_device_combo
        sub_frame_noise_cancellation_selector.columnconfigure(0, weight=5)
        sub_frame_noise_cancellation_selector.columnconfigure(1, weight=1)
        sub_frame_noise_cancellation_selector.grid(column=0, row=2, sticky=W+E, padx=(5, 0), pady=(0, 5))
        remove_noise_label = tk.Label(sub_frame_noise_cancellation_selector, text="Remove Noise", bg="white")
        remove_noise_label.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), sticky='e')
        remove_noise_selector = tk.Label(sub_frame_noise_cancellation_selector, text="Foo", bg="white")
        remove_noise_selector.grid(column=1, row=0, padx=(10, 10), pady=(10, 10), sticky='e')

        return frame

    def create_footer_frame(container):
        style = ttk.Style()
        style.configure("FOOTER.TLabel", background="#cdd1ce")
        frame = ttk.Frame(container, padding=0, relief='groove', style="FOOTER.TLabel")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        frame.email_label = tk.Label(frame, text="You have 240 minutes.", bg="#cdd1ce")
        frame.email_label.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), sticky='w')

        frame.mic_button: object = tk.Button(frame, relief="groove", text="upgrade", bg="#cdd1ce")
        frame.mic_button.grid(column=1, row=0, sticky="e", padx=(10, 10), pady=(10, 10))

        return frame

class Main_Form(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("app")
        self.geometry("400x550")
        self.resizable(0, 0)

        # Make Window Draggable
        self.bind("<ButtonPress-1>", self.StartMove)
        self.bind("<ButtonRelease-1>", self.StopMove)
        self.bind("<B1-Motion>", self.OnMotion)

        self.columnconfigure(0, weight=1)

        # Header Frame
        header_frame = Frame.create_header_frame(self)
        header_frame.grid(column=0, row=0, sticky=W+E)

        status_frame = Frame.create_statue_frame(self)
        status_frame.grid(column=0, row=1, sticky=W+E)

        input_frame = Frame.create_input_frame(self)
        input_frame.grid(column=0, row=2, padx=(10, 10), pady=(10, 10), sticky=W+E)

        input_frame = Frame.create_output_frame(self)
        input_frame.grid(column=0, row=3, padx=(10, 10), pady=(10, 10), sticky=W+E)

        footer_frame = Frame.create_footer_frame(self)
        footer_frame.grid(column=0, row=4, padx=(10, 10), pady=(10, 10), sticky=W+E)

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
