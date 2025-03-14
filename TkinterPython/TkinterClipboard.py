import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Get", command=self.on_button)
        self.button.pack()
        self.entry.pack()

    def on_button(self):
        self.clipboard_clear()
        self.clipboard_append(self.entry.get())
        print(self.entry.get())

app = SampleApp()
app.mainloop()
