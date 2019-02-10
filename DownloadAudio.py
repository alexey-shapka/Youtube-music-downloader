from __future__ import unicode_literals
import youtube_dl
from tkinter import *
from tkinter import messagebox
import webbrowser
import os

class Window:
    def __init__(self, root):
        self.main_window = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.last_link = ''
        self.path_to_save = os.path.dirname(os.path.abspath(__file__))
        self.main_window.title('Youtube Downloader')
        self.main_window.geometry("450x200+"+str(int(self.screen_width/2-450/2))+"+"+str(int(self.screen_height/2-200/2)))
        self.main_window.resizable(False, False)
        self.menu_bar = Menu(self.main_window)
        self.main_window.configure(menu=self.menu_bar)
        self.menu_bar.add_command(label="Path", command = self.ChangeWayFrame)
        self.main_window.bind('<Escape>', self.Exit)
        self.CreateMainframe()

    def ChangeWayFrame(self):
        self.path_frame = Toplevel()
        self.path_frame.geometry("400x135+"+str(int(self.screen_width/2-400/2))+"+"+str(int(self.screen_height/2-135/2)))
        self.path_frame.title("Change Path")
        self.path_frame.resizable(False, False)
        self.path_label = Label(self.path_frame, text="Path to save music", width=41, font=("Lato", 12), bg="#d6d6d6", fg="#3a3a3a")
        self.path_label.place(x=12, y=15)
        self.path_entry = Entry(self.path_frame, width=41, font=("Lato", 12), cursor="hand2", bg="#F0F0F0", fg="#3a3a3a")
        self.path_entry.place(x=13, y=55)
        self.path_entry.insert(0, self.path_to_save)
        self.path_button = Button(self.path_frame, width=30, text="Save", cursor="hand2", relief = 'raised', borderwidth=1, bg="#cecece", fg="#171714", font=("Lato", 10), activebackground="#FFFFFF", command=self.ChangePathToSaveFile)
        self.path_button.place(x=75, y=95)

    def CreateMainframe(self):
        self.label = Label(self.main_window, text="Input link", width=44, font=("Lato", 12), bg="#d6d6d6", fg="#3a3a3a")
        self.label.place(x=27,y=15)
        self.entry = Entry(self.main_window, width=44, font=("Lato", 12), cursor="hand2", bg="#F0F0F0", fg="#3a3a3a")
        self.entry.place(x=28,y=60)
        self.button = Button(self.main_window, width=35, text="Download", cursor="hand2", relief = 'raised', borderwidth=1, bg="#cecece", fg="#171714", font=("Lato", 10), activebackground="#FFFFFF", command=self.DownloadVideo)
        self.button.place(x=80, y=105)
        self.label_last_link = Label(self.main_window, width=44, font=("Lato", 12), bg="#d6d6d6", fg="#3a3a3a")
        self.main_window.update()

    def ClearMainFrame(self):
        self.label.place_forget()
        self.entry.place_forget()
        self.button.place_forget()
        self.main_window.update()

    def CreateDownloadFrame(self):
        self.upper_bound_decor =  Label(self.main_window,  width=56, bg = '#d6d6d6', font = ('Lato', 11))
        self.lower_bound_decor =  Label(self.main_window,  width=56, bg = '#d6d6d6', font = ('Lato', 11))
        self.download_label = Label(self.main_window, text="Downloading...", width=19, font=("Lato", 30, 'bold'), fg="#3a3a3a")
        self.download_label.place(x=0,y=75)
        self.upper_bound_decor.place(x=0, y=15)
        self.lower_bound_decor.place(x=0, y=165)
        self.main_window.update()

    def ClearDownloadFrame(self):
        self.download_label.place_forget()
        self.upper_bound_decor.place_forget()
        self.lower_bound_decor.place_forget()
        self.main_window.update()
    
    def CreateLastDownloadLabel(self, link):
        self.label_last_link = Label(self.main_window, text="Last: " + link, width=44, font=("Lato", 12), fg="#3a3a3a", cursor="hand2")
        self.label_last_link.place(x=27,y=155)
        self.label_last_link.bind("<Button-1>", self.Callback)

    def ClearLastDowloadLabel(self):
        self.label_last_link.place_forget()

    def Callback(self, event):
        webbrowser.open_new(self.last_link)

    def ChangePathToSaveFile(self):
        self.path_to_save = self.path_entry.get()

    def Exit(self, event):
        self.main_window.destroy()

    def DownloadVideo(self):
        self.ClearLastDowloadLabel()
        self.ClearMainFrame()
        self.CreateDownloadFrame()
        try:
            ydl_opts = {
            'outtmpl': '{}\%(title)s.%(ext)s'.format(self.path_to_save),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            }
            self.main_window.update()
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.entry.get()])

            self.last_link = self.entry.get()
            self.ClearDownloadFrame()
            self.CreateMainframe()
            self.CreateLastDownloadLabel(self.last_link)
            messagebox.showinfo("Success", "Successfully downloaded!")

        except:
            self.ClearDownloadFrame()
            self.CreateMainframe()
            
            if self.last_link != '':
                self.CreateLastDownloadLabel(self.last_link)
            messagebox.showinfo("Error", "Something went wrong..")

root = Tk()
q = Window(root)
root.mainloop()