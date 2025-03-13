import tkinter 
import customtkinter
from pytubefix import YouTube, Playlist

def checker(mode=0):
  try:
    ytLink = link.get()
    # ytLink = 'https://www.youtube.com/watch?v=RK27RX54EJU'
    # ytLink = 'https://www.youtube.com/playlist?list=PLQ56vaftymdpWoke1njSPFJBGfIBuPQQt'
    # print(ytLink)
    if mode == 4 or mode == "4a":
      playlist = Playlist(ytLink)
      title.configure(text=playlist.title)
      sizeP = len(playlist.video_urls)      
      print(sizeP, "videos")
      length = 0
      max_views = 0
      vid_name = ""
      for i,vid in enumerate(playlist.videos, 1):
        if mode == "4a":
          print(vid.watch_url)
        length += vid.length
        if vid.views > max_views:
          max_views = vid.views
          vid_name = vid.title
        percent_done = i/sizeP * 100
        percent_trunc = str(int(percent_done))
        pPercent.configure(text=f"{percent_trunc}%")
        pPercent.update()
        progressBar.set(percent_done / 100)
      print(f"Playlist Length: {length} seconds\nMost popular video: {vid_name} with: \n{max_views} views")
      vid_subinfo.configure(text=f"Videos: {sizeP}\nPlaylist Length: {length} seconds\nMost popular video in playlist: \n{vid_name}\n{max_views} views")
      finishLabel.configure(text="Completed!", text_color="green")
      print("Completed!")
      return
    ytObject = YouTube(ytLink, on_progress_callback=on_progress)
    info = f"Title: {ytObject.title}"
    title.configure(text=info)
    finishLabel.configure(text="")
    streamsV = ytObject.streams
    info = f"Author: {ytObject.author}\nLength: {ytObject.length} seconds\nViews: {ytObject.views}\nPublish Date: {ytObject.publish_date}\nstreams: {len(ytObject.streams)}"
    vid_subinfo.configure(text=info)
    if mode == 0:
      content = streamsV.get_highest_resolution()
    elif mode == 1:
      print(f"{info}\n{ytObject.channel_url}\n{ytObject.description}\n{ytObject.embed_url}\n{ytObject.thumbnail_url}")
      pPercent.configure(text=f"100%")
      progressBar.set(100)
      return
    elif mode == 2:
      content = streamsV.filter(progressive=False,video_codec="vp9").first()
    elif mode == 3:
      content = ytObject.streams.filter(only_audio=True).first()
    else:
      return    
    print(content)
    content.download()
  except Exception as e:
    # Handle errors gracefully
    finishLabel.configure(text="Link invalid or video error!", text_color="red")
    text=f"Error: {str(e)}",
    print(text)
    return
  finishLabel.configure(text="Completed!", text_color="green")
  print("Completed!")

def on_progress(stream, chunk, bytes_remaining):
  total_size = stream.filesize
  bytes_finished = total_size - bytes_remaining
  percent_done = bytes_finished / total_size * 100
  percent_trunc = str(int(percent_done))
  pPercent.configure(text=f"{percent_trunc}%")
  pPercent.update()
  progressBar.set(percent_done / 100)

def switchMode(value):
  if value == "Vid.":
    getVid.configure(command=checker)
  elif value == "Vid. only":
    getVid.configure(command=lambda: checker(2))
  elif value == "Aud. only":
    getVid.configure(command=lambda: checker(3))
  elif value == "Info.":
    getVid.configure(command=lambda: checker(1))
  elif value == "Playlist":
    getVid.configure(command=lambda: checker(4))
    getVidInfo.configure(command=lambda: checker("4a"))
# System config
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# frame
app = customtkinter.CTk()
app.geometry("480x480") # w x l
app.title("Youtube Info")

# UI element
# - input label text
title = customtkinter.CTkLabel(app, text="Enter a Youtube Link", wraplength=300)
title.pack(padx=10, pady=10)
# - <input/> element
url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url)
link.pack()
# - message element
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()
# - Options
my_options = customtkinter.CTkOptionMenu(app, values=["Vid.", "Playlist", "Vid. only","Aud. only", "Info."], command=switchMode)
my_options.pack(padx=10, pady=10)
# - getVid Button
getVid = customtkinter.CTkButton(app, text="Click to Check", command=checker)
getVid.pack(padx=10, pady=10)
# - getVidInfo Button
getVidInfo = customtkinter.CTkButton(app, text="Print to Console", command=lambda: checker(1), fg_color="green", hover_color="dark green")
getVidInfo.pack(padx=10, pady=10)
# - Info elements
vid_subinfo = customtkinter.CTkLabel(app, text="", justify="left")
vid_subinfo.pack()
# - Progress
pPercent = customtkinter.CTkLabel(app, text="0%")
pPercent.pack()
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# run app now
app.mainloop()

# resources: 
# https://www.youtube.com/watch?v=NI9LXzo0UY0 yt dl with modern gui
# https://www.youtube.com/watch?v=R1IiIAp8wAY tkinter options menu
# https://pytube.io/en/latest/user/playlist.html
# https://pytubefix.readthedocs.io/en/latest/
# https://customtkinter.tomschimansky.com/documentation/
# https://docs.python.org/3/library/tkinter.html