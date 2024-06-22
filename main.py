from views.main_window import MainWindow
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = MainWindow(root)
    root.mainloop()
