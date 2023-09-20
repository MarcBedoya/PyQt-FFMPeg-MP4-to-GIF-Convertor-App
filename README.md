# PyQt-MP4-to-GIF-Convertor-App

Python 3.11\
MP4 to GIF converter using FFMpeg and PyQt

--Currently only creates gifs at 24 FPS

#### Required:
Python library - cv2\
Python library - PySide6 (Qt for python)\
FFMpeg

## HOW TO USE
1. Click "Select MP4" and select the source video
2. Select the resolution factor (1:4 will output a gif at quarter resolution)\
   I don't know if any passed 1:8 are necessary but have at it
3. Click "Make GIF" and a gif will be output in the directory the source video is located in, and it will have the same name\
   **ex.** myvideo.mp4 -> myvideo.gif

## WARNING
This is only important if you *already* have a .gif file with the same name as the .mp4\
when a gif is created, the script will automatically override any gif with the same name, it will not ask.
