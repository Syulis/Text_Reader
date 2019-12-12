from PIL import Image
import pyocr
import pyocr.builders

import tkinter as tk
from tkinter import filedialog
import json
import re

class main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master.title("Text Reader")
        self.master.geometry("445x390")

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        menu_file = tk.Menu(self.master)
        menu.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Open", command=self.file_open, activebackground="blue")

        self.open_file = None

        self.log_box = tk.Entry(width=35)
        self.log_box.place(x=10, y=21.5)

        clear_button = tk.Button(text="All Clear")
        clear_button.place(x=230, y=19)
        clear_button.bind('<1>', self.all_clear)

        execution_button = tk.Button(text="Execution")
        execution_button.place(x=289, y=19)
        execution_button.bind('<1>', self.execution)

        copy_button = tk.Button(text="Copy")
        copy_button.place(x=357, y=19)
        copy_button.bind('<1>', self.copy)

        end_button = tk.Button(text="End")
        end_button.place(x=400, y=19)
        end_button.bind('<1>', self.end)

        self.text_box = tk.Text(width=60)
        self.text_box.place(x=10, y=65)

        self.file_open()

    def file_open(self):
        fld = filedialog.askopenfilename(initialdir="./text_images")
        self.open_file = fld
        if(self.open_file != 0):
            self.put_log("green", "Selected File")

    def all_clear(self, event):
        self.text_box.delete('0.0', tk.END)
        self.put_log("blue", "All Clear")

    def execution(self, event):
        try:
            tools = pyocr.get_available_tools()

            if(self.open_file == None):
                self.put_log("red", "No File Error")
                return

            if len(tools) == 0:
                self.put_log("red", "No OCR tool found")

            tool = tools[0]
            langs = tool.get_available_languages()
            lang = langs
            text = tool.image_to_string(
                Image.open(self.open_file),
                lang='jpn',
                builder=pyocr.builders.TextBuilder()
                )

            self.all_clear(event)
            self.text_box.insert(tk.END, text)
            self.put_log("blue", "Done")

        except:
            self.put_log("red", "Unexpected Error")
            return

    def copy(self, event):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.text_box.get('1.0', tk.END).strip())
        self.put_log("green", "Copied")

    def put_log(self, color, text):
        self.log_box.delete(0, tk.END)
        self.log_box.configure(fg=color)
        self.log_box.insert(tk.END, text)

    def end(self, event):
        self.master.destroy()

if __name__ == '__main__':
    f = main(None)
    f.pack()
    f.mainloop()
