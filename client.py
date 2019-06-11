import tkinter as tk


class QMS_Client:
    def __init__(self, root):
        frame1 = tk.Frame(root)
        hint = tk.Label(frame1, text='请输入当前办理号码：')
        hint.pack(side='top', padx=10, pady=10)
        self.cur_nubmer = tk.Entry(frame1)
        self.cur_nubmer.pack(side='top',padx=50,pady=10)
        frame1.pack()

        frame2 = tk.Frame(root)
        miss = tk.Button(frame2, text='过号', fg='red', command=self.miss_number)
        miss.pack(side='left',padx=10,pady=10)
        start = tk.Button(frame2, text='开始办理', fg='black', command=self.start_number)
        start.pack(side='left', padx=10, pady=10)
        done = tk.Button(frame2, text='完成', fg='green', command=self.finish_number)
        done.pack(side='left',padx=10,pady=10)
        frame2.pack()

        frame3 = tk.Frame(root)
        self.status = tk.Label(frame3, text='')
        self.status.pack(side='left')
        frame3.pack()

    
    def is_valid_num(self, string_to_check):
        if not string_to_check:
            return False
        for c in string_to_check:
            if c not in '0123456789':
                return False
        return True
    def start_number(self):
        num = self.cur_nubmer.get().strip()
        if not self.is_valid_num(num):
            self.status['text'] = '输入号码无效！'
            self.cur_nubmer.delete(0, tk.END)
            return
        # self.cur_nubmer.delete(0, tk.END)
        self.status['text'] = '正在为{}号办理业务...'.format(num)

    def miss_number(self):
        num = self.cur_nubmer.get().strip()
        if not self.is_valid_num(num):
            self.status['text'] = '输入号码无效！'
            self.cur_nubmer.delete(0, tk.END)
            return
        self.cur_nubmer.delete(0, tk.END)
        self.status['text'] = '{}号已过号！'.format(num)

    def finish_number(self):
        num = self.cur_nubmer.get().strip()
        if not self.is_valid_num(num):
            self.status['text'] = '输入号码无效！'
            self.cur_nubmer.delete(0, tk.END)
            return
        self.cur_nubmer.delete(0, tk.END)
        self.status['text'] = '{}号已完成！'.format(num)

root = tk.Tk()
root.title('排号系统')
app = QMS_Client(root)
root.mainloop()