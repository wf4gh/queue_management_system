import tkinter as tk

class QMS_Server:
    def __init__(self, root):
        frame1 = tk.Frame(root)
        processing = tk.Label(frame1, text='当前正在办理：')
        processing.pack(side='top',padx=50,pady=5)
        frame1.pack()

        frame2 = tk.Frame(root)
        lst_processing = tk.Listbox(root)
        lst_processing.pack(side='top')
        frame2.pack()

        frame3 = tk.Frame()
        waiting = tk.Label(frame3, text='当前等待办理：')
        waiting.pack(side='top')
        frame3.pack()

        frame4 = tk.Frame()
        lst_waiting = tk.Listbox(root)
        lst_waiting.pack(side='top')
        frame4.pack()


root = tk.Tk()
root.title('办理进度')
app = QMS_Server(root)
root.mainloop()