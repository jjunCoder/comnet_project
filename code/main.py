import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(누르세요)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.txt_input = tk.Entry(self)
        self.txt_input.pack()

        self.send_btn = tk.Button(self, text="Send", fg="green", command=self.send_btn)
        self.send_btn.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

    def send_btn(self):
        print("msg send stub.")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
