import tkinter as tk
# import socket


class QMS_Server:
    def __init__(self, root):
        frame1 = tk.Frame(root)
        self.w1 = tk.Label(frame1, text=self.gen_text(1, 1))
        self.w1.pack(side='top', padx=50, pady=5)
        self.w2 = tk.Label(frame1, text=self.gen_text(2, 2))
        self.w2.pack(side='top', pady=5)
        self.w3 = tk.Label(frame1, text=self.gen_text(3, 3))
        self.w3.pack(side='top', pady=5)
        self.w4 = tk.Label(frame1, text=self.gen_text(4, 4, ''))
        self.w4.pack(side='top', pady=5)
        # self.w5 = tk.Label(frame1, text=self.gen_text(5, 5, ''))
        # self.w5.pack(side='top',pady=5)
        frame1.pack()

        # always on top
        root.attributes('-topmost', 'true')

        


        # self.s_sock = socket.socket()
        # host = socket.gethostname()
        # port = 1611
        # self.s_sock.bind((host, port))

        # root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # def listen_sock(self):
    #     self.s_sock.listen(5)
    #     while True:
    #         c_sock, addr = self.s_sock.accept()
    #         print(addr)
    #         c_sock.send('info send from s_sock')
    #         c_sock.close()

    def gen_text(self, window_num, cur_num, type='doing'):
        if type == 'doing':
            text = '{}号窗口: 正在为{}号办理'.format(window_num, cur_num)
        else:
            text = '{}号窗口: 正在等待{}号...'.format(window_num, cur_num)
        return text

    # def on_closing(self):
    #     self.s_sock.shutdown()
    #     # self.s_sock.close()

root = tk.Tk()
root.title('办理进度')
server = QMS_Server(root)
root.mainloop()
# server.listen_sock()
