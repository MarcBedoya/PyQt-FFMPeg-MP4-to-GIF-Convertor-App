#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Marc B
#9/20/23 12:50 AM

import sys
import subprocess
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

#need to install
import cv2
from PySide6.QtWidgets import (QApplication, QPushButton, QWidget, QMainWindow, QLabel, QVBoxLayout, QComboBox)
from PySide6.QtCore import (QObject, Signal, Slot)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        #initializing some variables
        self.file_path = ""
        self.resolution = ""
        
        #Creating dropdown menu
        self.res_select = QComboBox()
        self.res_list = ['1:1', '1:2', '1:4', '1:8', '1:16', '1:32', '1:64?', '1:128??', '1:256...', '1:512. Really?']
        #Created list of all elements to add and added them all at once
        self.res_select.addItems(self.res_list)
                    
        #initializing qWidget and customizing the window
        widget = QWidget()
        widget.setFixedSize (500,150)
        widget.setWindowTitle('GIF Maker')
        self.setCentralWidget(widget)
        
        #Creating labels
        self.label = QLabel("GIF Maker")
        self.label2 = QLabel("Select resolution ratio")
        
        #Creating QBoxLayout container for widgets
        layout = QVBoxLayout(widget)
        
        #creating button widgets and assigning functions to each
        file_button = QPushButton(text = 'Select MP4')
        file_button.clicked.connect(self.file_browse)
        
        gif_button = QPushButton(text = 'Make GIF')
        gif_button.clicked.connect(self.make_gif)
        
        #adding widgets in order i want stacked in the vertical layout
        layout.addWidget(self.label)
        layout.addWidget(file_button)
        layout.addWidget(self.label2)
        layout.addWidget(self.res_select)
        layout.addWidget(gif_button)
        
        #displays the MainWindow
        self.show()

    #Function that uses tkinter to get the name of a file based on user input
    @Slot()
    def file_browse(self):
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename()

    #Function that uses FFMpeg via direct command line input; limited to very specific commands
    @Slot()
    def make_gif(self):
        #parses the file directory that the selected file is in from the full file path
        filedir = os.path.dirname(self.file_path)
        #parses the name of the file itself from the full file path
        output_name = Path(self.file_path).stem
        
        #Calculates the factor by which to reduce the resolution of the video
            #since the resolutions are sequential in the drop menu, i can calculate the factor based on the index of the item in the list
            #1:16 is the 5th item in the menu, 2^(n-1) -> 2^(5-1) = 16. Index starts at 0 so -1 isn't necessary in actual code
        res_select = pow(2, self.res_select.currentIndex())
        
        #gets width of source video
        res_w = cv2.VideoCapture(self.file_path).get(cv2.CAP_PROP_FRAME_WIDTH)
        
        #Res of source / factor. If 1920x1080 at 1:2, (1920/2) = 960, gif output will have a width of 960 in same aspect ratio
        resolution = res_w/res_select
        
        #first FFMpeg command. This generates a color palette that will be used to help generate the gif
        #pass variables at end  where there is %s
        p_cmd = 'ffmpeg -i %s -filter_complex "[0:v] palettegen" pyqtgifpalettetemp.png -y' % (self.file_path) 
        
        #second FFMpeg command. Generates the gif at the resolution specified
        #FPS can be made to be customized, but for now forced 24 fps
        #Scale input is w:h, when h = -1, it maintains the aspect ratio so I only need one value
        m_cmd = 'ffmpeg -i %s.mp4 -i pyqtgifpalettetemp.png -filter_complex "[0:v] fps=24,scale=%s:-1 [new];[new][1:v] paletteuse" %s.gif -y' % (output_name, resolution, output_name)
        
        #Deletes the color palette, normal commond
        c_cmd = 'del pyqtgifpalettetemp.png'
        
        #Sets the working directory for all the FFMpeg commands to the directory which the source video is taken from
        filedir = os.path.dirname(self.file_path)
        
        #Execute each process and wait for them to complete before beginning the next
        proc1 = subprocess.Popen(p_cmd, shell=True, cwd = filedir)
        proc1.wait()
        proc2 = subprocess.Popen(m_cmd, shell=True, cwd = filedir)
        proc2.wait()
        proc3 = subprocess.Popen(c_cmd, shell=True, cwd = filedir)
        proc3.wait()

#Main python functions
#Initialize app and execute it
app = QApplication(sys.argv)
main_window = MainWindow()
app.exec()


# In[ ]:




