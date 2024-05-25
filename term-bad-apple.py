#!/bin/python
from pytube import YouTube
from os import path
from shutil import get_terminal_size
from moviepy.editor import VideoFileClip
from playsound3 import playsound
import cv2
import time

BAD_APPLE_YT_ID: str = "FtutLA63Cp8"
BAD_APPLE_LINK: str = "https://www.youtube.com/watch?v=" + BAD_APPLE_YT_ID


print("- Starting")
if not path.exists('bd-appl.mp4'):
    try:
        print("- Creating pytube object")
        yt = YouTube(BAD_APPLE_LINK)
        stream = yt.streams.get_highest_resolution()

        print("- Downloading bad apple")
        stream.download(filename="bd-appl.mp4")  # pyright: ignore
        print("- Download complete")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("- Using already downloaded bad apple")

print("- Extracting audio")
if not path.exists('bd-appl-aud.mp3'):
    try:
        clip = VideoFileClip("bd-appl.mp4")
        audio = clip.audio
        audio.write_audiofile("bd-appl-aud.mp3")  # pyright: ignore
    except Exception as e:
        print(f"Error: {e}")
else:
    print("- Using already extracted audio")

print("- Getting stuff ready")
ASCII_CHARS = "@%#*+=-:. "
BAD_APPLE_SOURCE = cv2.VideoCapture("bd-appl.mp4")

FPS = 44

print("- Playing audio")
playsound("bd-appl-aud.mp3", block=False)

while True:
    print("\033c", end="")

    ret, img = BAD_APPLE_SOURCE.read()
    if not ret:
        break

    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t_size = get_terminal_size()
    width, height = t_size.columns, t_size.lines
    height = min(height - 1, grayscale.shape[0])
    width = min(width, grayscale.shape[1])
    resized = cv2.resize(grayscale, (width, height),
                         interpolation=cv2.INTER_AREA)

    img_shape = resized.shape

    for y in range(height):
        line = ''
        for x in range(width):
            line += ASCII_CHARS[min(resized[y, x] // 32, len(ASCII_CHARS) - 1)]
        print(line)

    delay_time = 1 / FPS
    time.sleep(delay_time)

BAD_APPLE_SOURCE.release()
