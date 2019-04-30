import math
import string
import secrets #requires Python 3.6
import random
import tkinter as tk

class PassGenerator(tk.Tk):
    def __init__(self):
        width = '400'
        height = '100'
        tk.Tk.__init__(self)
        self.geometry('{}x{}'.format(width, height))
        self.title("Password Generator")
        self.label= tk.Label(self, text="Password: ")
        self.resizable(False, False)
        self.entry = tk.Entry(self, width=30, justify="center")
        self.entry.config(bg=self.cget('bg'), relief="flat")
        self.button = tk.Button(self, text="Copy Password to Clipboard", command=self.CopyToClipboard)
        self.button2 = tk.Button(self, text="Generate Password", command=self.genPassword)
        
        #draw elements

        self.label.pack()
        self.entry.pack()
        self.button2.pack()
        self.button.pack()


    def CopyToClipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.entry.get())
        self.update()

    def genPassword(self, length=20, mode=0):
        self.entry.delete(0,"end")
        if mode == 0: #All Punctuation, Upper/Lower, and digits
            alpha = string.punctuation + string.ascii_letters + string.digits
        elif mode == 1: #All UpperLower and Digits
            alpha = string.ascii_letters + string.digits
        elif mode == 2: #All UpperLower
            alpha = string.ascii_letters
        setSize = len(alpha)
        length = math.ceil(random.uniform(length-5,length+5))
        password = ''.join(secrets.choice(alpha) for i in range(length))
        self.entry.insert(1, password.strip())

app = PassGenerator()
app.mainloop()
