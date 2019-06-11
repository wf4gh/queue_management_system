import tkinter as tk

class QMS_Server:
    def __init__(self, root):
        frame1 = tk.Frame(root)
        self.w1 = tk.Label(frame1, text=self.gen_text(1, 1))
        self.w1.pack(side='top',padx=50,pady=5)
        self.w2 = tk.Label(frame1, text=self.gen_text(2, 2))
        self.w2.pack(side='top',pady=5)
        self.w3 = tk.Label(frame1, text=self.gen_text(3, 3))
        self.w3.pack(side='top',pady=5)
        self.w4 = tk.Label(frame1, text=self.gen_text(4, 4))
        self.w4.pack(side='top',pady=5)
        self.w5 = tk.Label(frame1, text=self.gen_text(5, 5, ''))
        self.w5.pack(side='top',pady=5)
        frame1.pack()

    def gen_text(self, window_num, cur_num, type='doing'):
        if type == 'doing':
            text = '{}号窗口: 正在为{}号办理'.format(window_num, cur_num)
        else:
            text = '{}号窗口: 正在等待{}号...'.format(window_num, cur_num)
        return text

root = tk.Tk()
root.title('办理进度')
app = QMS_Server(root)
root.mainloop()
