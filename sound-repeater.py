### Developed by H.Can Ataç - TA2CCN

import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from threading import Thread
import time

class RepeatPlayer:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        pygame.init()
        self.is_playing = False
        self.thread = None
        self.filename = None

    def setup_gui(self):
        self.root.title("Sound Repeater v1.0")
        self.root.geometry("300x200")  # Pencere boyutunu 300x200 olarak ayarladık
        self.root.resizable(False, False)

        self.select_button = tk.Button(self.root, text="Select a sound file", command=self.select_file)
        self.select_button.pack(pady=10)

        self.interval_label = tk.Label(self.root, text="Time Interval (Minutes):")
        self.interval_label.pack()

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack()
        self.interval_entry.insert(0, "1")

        self.start_button = tk.Button(self.root, text="Start", command=self.start_playing)
        self.start_button.pack(pady=20)

    def select_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
        if self.filename:
            print("Choosen file:", self.filename)

    def start_playing(self):
        if not self.is_playing:
            try:
                interval = int(self.interval_entry.get())
                if not self.filename or interval <= 0:
                    raise ValueError("Invalid file or time interval!")
                self.is_playing = True
                self.start_button.config(text="Exit", command=self.on_closing)
                self.thread = Thread(target=self.repeat_play, args=(interval,))
                self.thread.daemon = True  # Arka plan iş parçacığını daemon olarak ayarla
                self.thread.start()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid file and/or time interval!")
                self.interval_entry.focus_set()

    def repeat_play(self, interval):
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        while self.is_playing:
            time.sleep(interval * 60)  # Dakikayı saniyeye çevir
            if not self.is_playing:
                break
            pygame.mixer.music.play()

    def on_closing(self):
        self.is_playing = False
        pygame.mixer.music.stop()
        self.root.destroy()  # İş parçacığının bitmesini beklemeden pencereyi kapat

if __name__ == "__main__":
    root = tk.Tk()
    app = RepeatPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
