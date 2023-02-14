import vlc
import time
import json
import tkinter as tk
from PIL import ImageTk, Image
import os
import requests

open("radios.json", "w").write(requests.get("https://raw.githubusercontent.com/BLINMATIC/OpenRadioCLI/main/data/radios.json").text)

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x229")
        self.root.resizable(width=False, height=False)
        self.selector = 0

        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()
        self.radios = json.loads(open("radios.json", "r").read())

        self.previous = tk.Button(self.root, text="⏮", width=2, padx=2, height=1, command=lambda: self.prev_())
        self.next     = tk.Button(self.root, text="⏭", width=2, padx=2, height=1, command=lambda: self.next_())
        self.play     = tk.Button(self.root, text="▶️", width=2, padx=2,height=1, command=lambda: self.player.play())
        self.stop     = tk.Button(self.root, text="⏹", width=2, padx=2,height=1, command=lambda: self.player.stop())
        self.pause    = tk.Button(self.root, text="⏯", width=2, padx=2,height=1, command=lambda: self.player.pause())
        self.radio_name = tk.StringVar()
        self.radio_name.set("")
        self.radio = tk.Label(self.root, textvariable=self.radio_name)

        self.previous.place(x=0, y=0)
        self.next.place(x=25, y=0)
        self.play.place(x=50, y=0)
        self.stop.place(x=75, y=0)
        self.pause.place(x=100, y=0)
        self.radio.place(x=126, y=2)
        open("img.png", "wb").write(requests.get("https://th.bing.com/th/id/OIP.qrmUaxLP2JaX7mguXidu3wAAAA?pid=ImgDet&rs=1").content)
        img = ImageTk.PhotoImage(Image.open("img.png").resize((300, 200)))
        self.image = tk.Label(self.root, image=img)
        self.image.place(x=0, y=26)

        self.load(self.radios[0]["url"])

        self.root.mainloop()

    def load(self, url: str):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.radio_name.set(self.radios[self.selector]["name"])

        open("img.png", "wb").write(requests.get(self.radios[self.selector]["image"]).content)
        img = ImageTk.PhotoImage(Image.open("img.png").resize((300, 200)))

        self.image.configure(image=img)
        self.image.image = img

    def next_(self):
        try:
            self.player.stop()
            self.selector += 1
            self.load(self.radios[self.selector]["url"])
            self.player.play()
        except:
            self.player.play()

    def prev_(self):
        try:
            self.player.stop()
            self.selector -= 1
            self.load(self.radios[self.selector]["url"])
            self.player.play()
        except:
            self.player.play()

if __name__ == "__main__":
    m = Main()
