import customtkinter as ctk

from memo import Memo

ctk.set_appearance_mode("light")

if __name__ == '__main__':
    app = ctk.CTk()
    app.geometry("450x640")
    app.wm_title("TKINTER TEXT EDITOR")
    app.resizable(False, False)
    memo = Memo(app, height=350, width=350, fg_color="white")
    #center(app)
    memo.pack()
    app.mainloop()