from pytube import YouTube, Playlist
from moviepy.editor import *
import re

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

    os.remove(audio_file)
    print(youtube_video.title+".mp3 converted")
    print()

def is_valid(link:str):
    if re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', link):
        return True
    print("Error: Invalid YouTube link")
    return False


def main():
    link = input("Enter a Youtube Video or Playlist link: ")
    if is_valid(link):
        convert_to_mp3(link)
        return
    print("Please enter a valid link\n")
    main()

main()

