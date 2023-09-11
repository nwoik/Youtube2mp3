from tkinter import *
from pytube import YouTube, Playlist
from moviepy.editor import *
import re

def on_focus_in(entry:Entry):
    if entry.cget('state') == 'disabled':
        entry.configure(state='normal')
        entry.delete(0, 'end')

def on_focus_out(entry:Entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.configure(state='disabled', disabledbackground="white", disabledforeground="grey")

def text_insert(widget:Widget, text:str):
    widget.configure(state="normal")
    widget.insert(INSERT, text+"\n")
    widget.configure(state="disabled")
    return text

def text_highlighting(textbox:Text, text:str):
    lines = textbox.get("1.0", END).count("\n")-1
    textbox.tag_add("title", f"{lines}.10", f"{lines}.{(10+(len(text)+2))}")
    textbox.tag_add("mp3", f"{lines}.{(10+(len(text)+6))}", f"{lines}.{(10+(len(text)+9))}")


def convert_to_mp3(link:str):
    if "playlist" in link:
        for video in Playlist(link):
            extract_audio(video)
    else:
        extract_audio(link)

def extract_audio(link:str):
    youtube_video = YouTube(link)
    audio_stream = youtube_video.streams.filter(only_audio=True).first()

    audio_file = audio_stream.download()

    audio_clip = AudioFileClip(audio_file)
    audio_clip.write_audiofile(audio_file[:-4] + ".mp3")
    text_insert(text_output, "Converted '%s' to mp3" % youtube_video.title)
    text_highlighting(text_output, youtube_video.title)

    os.remove(audio_file)


def is_valid(link:str):
    if re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
        return True
    return False

def get_input():
    link = text_input.get()
    if is_valid(link):
        convert_to_mp3(link)
        return
    text_insert(text_output, "Please enter a valid link")


root = Tk()

root.geometry("800x500")
width = root.winfo_width()
height = root.winfo_height()
root.title("Youtube2Mp3")

text_input = Entry(root, width=50)
text_input.insert(0, "Enter a Youtube Link")
text_input.configure(state='disabled', disabledbackground="white", disabledforeground="grey")
x_focus_in = text_input.bind('<Button-1>', lambda x: on_focus_in(text_input))
x_focus_out = text_input.bind('<FocusOut>', lambda x: on_focus_out(text_input, 'Enter a Youtube Link'))

text_output = Text(root, width=90, bg="white")
text_output.configure(state="disabled")
text_output.tag_configure("title", foreground="blue")
text_output.tag_configure("mp3", foreground="green")

button = Button(root, text="Convert", command=get_input)

text_input.place(x=195, y=30)
button.place(x=500, y=26)
text_output.place(x=35, y=70)


root.resizable(False, False)
root.mainloop()
