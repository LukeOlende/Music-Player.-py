import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()           # Returns a list of all themes that can be set
root.set_theme("radiance")  #Sets an available theme

#Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman(Times) and Verdana

# Styles - normal, bold, roman, italic, underline, and overstrike

statusbar = ttk.Label(root, text="Welcome to Mziki", relief=SUNKEN, anchor=W, font = "Times 10 bold")
statusbar.pack(side=BOTTOM, fill=X)

# create a menu bar
menubar = Menu(root)
root.config(menu = menubar)

# create the sub-menu

subMenu = Menu(menubar, tearoff=0)

playlist = []


# Playlist -  contains the full path + filename
# PlaylistBox - contains filename
# Fullpath + filename is required to play the music inside play_music function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistBox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('Mziki Music Player',
                                'This is a music player app built using Python Tkinter by @Luke Olende.')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer


root.title("Mziki Player")
root.iconbitmap(r'Images/melody.ico')

# Root Window - StatusBar, leftFrame and rightFrame
# leftFrame - The listBox (Playlist)
# rightFrame - The TopFrame, MiddleFrame and BottomFrame
leftFrame = Frame(root)
leftFrame.pack(side = LEFT, padx = 30, pady = 30)

playlistBox = Listbox(leftFrame)
playlistBox.pack()

addBtn = ttk.Button(leftFrame, text = " + ADD", command = browse_file)
addBtn.pack(side = LEFT)

def del_song():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)

delBtn = ttk.Button(leftFrame, text = " - DEL", command = del_song)
delBtn.pack(side = LEFT)

rightFrame = Frame(root)
rightFrame.pack(pady = 30)

topFrame = Frame(rightFrame)
topFrame.pack()

lengthLabel = ttk.Label(topFrame, text="Total Length - --:--", font = "Arial 10 bold")
lengthLabel.pack(pady = 5)

CurrentTimeLabel = ttk.Label(topFrame, text="Current Time - --:--", relief = GROOVE, font = "Arial 10 bold", )
CurrentTimeLabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()


    #div - total_length / 60  mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Total Length" + " - " + timeFormat

    t1 = threading.Thread(target= start_count, args=(total_length, ))
    t1.start()

def start_count(t):
    global paused
    # mixer.music.get_busy() - Returns FALSE when we press the stop button or music stops playing
    # continue - ignores all the code below it. We check if music is paused or not
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = '{:02d}:{:02d}'.format(mins, secs)
            CurrentTimeLabel['text'] = "Current Time" + " - " + timeFormat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistBox.curselection()
            selected_song = int(selected_song[0])
            play_it =playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + "-" + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Mziki could not find the file! Please check again!')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music has been stopped"

paused = FALSE

def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music has been paused"
def rewind_music():
    mixer.music.rewind()
    statusbar['text'] = "Music rewinded"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

muted = FALSE

def mute_music():
    global muted
    if muted: # Unmute the music
        mixer.music.set_volume(0.5)
        VolumeBtn.configure(image=VolumePhoto)
        scale.set(50)
        muted = FALSE
    else: # mute the music
        mixer.music.set_volume(0)
        VolumeBtn.configure(image=MutePhoto)
        scale.set(0)
        muted = TRUE


middleFrame = Frame(rightFrame)
middleFrame.pack(padx = 30, pady = 30)

PlayPhoto = PhotoImage(file='Images/play.png')
playBtn = ttk.Button(middleFrame, image=PlayPhoto, command=play_music)
playBtn.grid(row = 0, column = 0,padx = 10)

PausePhoto = PhotoImage(file='Images/pause.png')
PauseBtn = ttk.Button(middleFrame, image=PausePhoto, command=pause_music)
PauseBtn.grid(row = 0, column = 1,padx = 10)

StopPhoto = PhotoImage(file='Images/stop.png')
StopBtn = ttk.Button(middleFrame, image=StopPhoto, command=stop_music)
StopBtn.grid(row = 0, column = 2,padx = 10)

# Bottom frame for rewind, mute and volume
bottomFrame = Frame(rightFrame)
bottomFrame.pack()

RewindPhoto = PhotoImage(file='Images/rewind.png')
RewindBtn = ttk.Button(bottomFrame, image=RewindPhoto, command=rewind_music)
RewindBtn.grid(row = 0, column = 0)

MutePhoto = PhotoImage(file='Images/mute.png')
VolumePhoto = PhotoImage(file='Images/volume.png')
VolumeBtn = ttk.Button(bottomFrame, image=VolumePhoto, command=mute_music)
VolumeBtn.grid(row = 0, column = 1)

scale = ttk.Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50) #impliment the defaut value of scale when the player starts
mixer.music.set_volume(0.5)
scale.grid(row = 0, column = 2, pady = 15, padx = 30)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
