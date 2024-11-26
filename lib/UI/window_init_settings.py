import sys
sys.path.insert(1, 'E:\PG\Projects\PAOL\python-paol')

import os
os.environ["OPENCV_LOG_LEVEL"] = "debug" # value must be a string
os.environ["OPENCV_VIDEOIO_DEBUG"] = "1" # value must be a string

import platform

import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import Image as Im
from PIL import ImageTk

import threading
import cv2
import subprocess
from typing import List

import lib.paol_utils as utils
import lib.camera_utils.Camera as Camera

NO_SELECTION = {
    'NONE':0
}

SELECTIONS = {
    'NOT_SET':0,
    'DISABLED':1,
    'LECTURE(w/ AUDIO)':2,
    'WHITEBOARD':3,
    'BLACKBOARD':4,
    'COMPUTER':5,
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SettingScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        utils.log('INFO', 'Creating Defaults...')
        # Defaults
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        #New Camera Settings
        self.cameras = [] #Camera Array
        self.display_resolution = self.get_res()
        self.display_camera_thread = None #replace thread
        self.display_camera_thread_stop_event = None #replace stop_event
        self.options_display_camera_names = [] #replace video_panel_names
        self.display_image = []

        utils.log('INFO', 'Defaults Created.')
        utils.log('INFO', 'Creating Window...')

        # Window Config
        self.title("Settings")
        self.geometry(f"{600}x{400}")

        # Grid Config
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1), weight=1)

        # Side Bar Settings
        self.init_sidebar()

        # Main Frame Settings
        self.init_mainframe()

        utils.log('INFO', 'Window Created.')
        utils.log('INFO', 'Searching for available video devices...')

        # Run Camera Connections on a separate thread
        cameras_thread = threading.Thread(target=self.init_cameras)
        cameras_thread.start()

    #SCREEN BUILDING FUNCTIONS =========================================
    def init_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
#
        self.optionmenu_var = ctk.StringVar(value="Dark")
#
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event,
                                                                       variable = self.optionmenu_var)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

    def init_mainframe(self):
        # Main Frame Settings
        self.mainframe = ctk.CTkFrame(self, corner_radius=0 )
        self.mainframe.grid(row=0, column=1, sticky=(N,W,E,S))
        self.mainframe.grid_rowconfigure(0, weight=1)

        # Main Frame Title
        self.mainframe_title_text = "Camera Settings"
        self.mainframe_title_font = ctk.CTkFont(family="Times>", size=30, weight="bold")
        self.mainframe_title = ctk.CTkLabel(self.mainframe, text=self.mainframe_title_text, fg_color="gray30", font=self.mainframe_title_font, corner_radius=6)
        self.mainframe_title.grid(row=0, column=1, columnspan=4, sticky="nsew")

        # sub Main Frame Settings
        self.subframe = ctk.CTkFrame(self.mainframe, corner_radius=0 )
        self.subframe.grid(row=1, column=1, columnspan=4, sticky="nsew")

        #Choose Camera to set
        # Main Frame Title
        self.camera_options_title_text = "Camera Options: "
        self.camera_options_title_font = ctk.CTkFont(family="Times>", size=12, weight="bold")
        self.camera_options_title = ctk.CTkLabel(self.subframe, text=self.camera_options_title_text, fg_color="gray30", font=self.camera_options_title_font, corner_radius=6)
        self.camera_options_title.grid(row=0, column=0)
        self.camera_options_title.grid_columnconfigure(0, weight=1)

        self.camera_options_var_selected = [*NO_SELECTION][0] #str
        self.camera_options_var = ctk.StringVar(value=[*NO_SELECTION][0])
        self.camera_options = ctk.CTkOptionMenu(self.subframe, values=[*NO_SELECTION],
                                                command=self.on_camera_displayed_change,
                                                variable=self.camera_options_var)
        self.camera_options.grid(row=0, column=1)
        self.camera_options.grid_columnconfigure(1, weight=1)

        #TODO: Add Selection option for THIS camera - so likely add it to Camera()

        self.init_camera_display()
        
    def init_camera_display(self):
        self.camera_display = Label(self.subframe, image=self.display_image)
        self.camera_display.image = self.display_image
        self.camera_display.grid(row=1, column=0, columnspan=8, pady=20)

    #CAMERA FUNCTIONS =========================================
    def init_cameras(self):
        # Clear previous Data
        self.options_display_camera_names.clear()

        # Get Camera Info
        self.collect_cameras()
        sorted(self.cameras, key=lambda camera: camera.Index)

        utils.log('INFO', 'Found ' + str(len(self.cameras)) + ' video devices:')
        
        self.update_camera_options()
        self.start_camera_display()

    def update_camera_options(self):
        # Get Names for OptionMenu
        for i in range(len(self.cameras)):
            self.options_display_camera_names.append(str(self.cameras[i].Index))

        # Update OptionMenu
        self.camera_options.configure(True, values=self.options_display_camera_names)
        self.set_camera_displayed(self.options_display_camera_names[0])

    def start_camera_display(self):
        # Create Event to stop thread
        self.display_camera_thread_stop_event = threading.Event()
        
        # Get the current selected index of Camera
        try:
            selected_index = int(self.camera_options_var_selected)
        except ValueError:
            selected_index = 0

        if len(self.cameras) > 0 and len(self.cameras) > selected_index:
            selected_camera = self.cameras[selected_index]
            selected_camera.Frames.append(None)
            
            # Start camera thread
            self.display_camera_thread = threading.Thread(target=self.single_camera_video_loop, args=(selected_index,))
            self.display_camera_thread.start()

    def update_camera_display(self):
        if self.display_camera_thread_stop_event is not None:
            self.display_camera_thread_stop_event.set() #Kill current camera thread

        self.start_camera_display()

    def collect_cameras(self):
        for i in range(10):  # Check up to 10 cameras
            new_camera = Camera.Camera()
            new_camera.Capture = cv2.VideoCapture(i)
            if new_camera.Capture.isOpened():
                new_camera.Index = i
                self.cameras.append(new_camera)
    
    def single_camera_video_loop(self, *args):
        f = open("./logs/gui_err.log", "w+")
        sto = sys.stderr
        sys.stderr = f
        i = args[0]

        selected_index = int(self.camera_options_var_selected)
        camera = self.cameras[selected_index]
        if(camera is None):
            utils.log('INFO', 'Camera Not Valid')
            pass
        
        try:
            # keep looping over frames until we are instructed to stop
            while not self.display_camera_thread_stop_event.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of WIDTH/count pixels
                ret, camera.Frame = camera.Capture.read()
                # utils.log('INFO', 'Captured size'+ str(self.frames[i].shape))
                ratio = ((1.0 * self.display_resolution[0])/(1))/camera.Frame.shape[0]
                # utils.log('INFO', 'Ratio: ' + str(ratio))
                camera.Frame = cv2.resize(camera.Frame, (int(camera.Frame.shape[1]*ratio), int(camera.Frame.shape[0]*ratio)))
                # utils.log('INFO', 'Resized: ' + str(self.frames[i].shape))

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                self.display_image = cv2.cvtColor(camera.Frame, cv2.COLOR_BGR2RGB)
                self.display_image = Im.fromarray(self.display_image)
                self.display_image = ImageTk.PhotoImage(self.display_image)

                # if the panel is not None, we need to initialize it
                if self.camera_display is None:
                    self.camera_display = Label(self.subframe, image=self.display_image)
                    self.camera_display.image = self.display_image
                    self.camera_display.grid(row=1, column=0)

                # otherwise, simply update the panel
                else:
                    self.camera_display.configure(image=self.display_image)
                    self.camera_display.image = self.display_image
            exit
        except RuntimeError as e:
            utils.log('WARN', 'RuntimeError on GUI.')
            utils.log('INFO', 'Check logs/gui_err.log for details.')

    #UTIL FUNCTIONS =========================================
    def get_res(self):
        if platform.system() == "Linux":
            output = subprocess.Popen('xrandr | grep \* | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
            resolution = output.split()[0].split(b'x')
            utils.log('INFO', 'Resolution: ' + str(int(resolution[0])) + 'x' + str(int(resolution[1])))
            return int(resolution[0]), int(resolution[1])
        if platform.system() == "Windows":
            return int(600), int(400) #TODO: Replace when working
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        self.optionmenu_var.set(new_appearance_mode)
        ctk.set_appearance_mode(self.optionmenu_var.get())

    def set_camera_displayed(self, new_display_index:str):
        self.camera_options_var.set(new_display_index)
        self.camera_options_var_selected = new_display_index

    def on_camera_displayed_change(self, new_display_index:str):
        self.camera_options_var_selected = new_display_index
        self.update_camera_display()

    #GENERAL WINDOW FUNCTIONS =========================================
    def on_close(self):
        utils.log('INFO', 'Closing SETUP Window...')

        if self.display_camera_thread_stop_event is not None:
            self.display_camera_thread_stop_event.set()

        self.quit()
        self.destroy()
        sys.exit()

# ==========================================================================================

if __name__ == "__main__":
    app = SettingScreen()
    app.mainloop()