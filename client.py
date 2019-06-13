import tkinter as tk
# from tkinter import messagebox
import socket
import sys
import settings

HOST = settings.SERVER_HOST
PORT = settings.SERVER_PORT
CUR_WINDOW_NAME = settings.CLIENT_HOST[settings.WINDOW_IP]

# numbers = settings.NUMS


class QMS_Client:
    def __init__(self, root):
        frame_input = tk.Frame(root)
        hint = tk.Label(frame_input, text='请输入当前办理号码：')
        hint.pack(side='top', padx=10, pady=10)
        self.cur_nubmer = tk.Entry(frame_input)
        self.cur_nubmer.pack(side='top', padx=50, pady=10)
        frame_input.pack()

        frame_buttons = tk.Frame(root)
        miss = tk.Button(frame_buttons, text='过号',
                         fg='red', command=self.click_miss_number)
        miss.pack(side='left', padx=10, pady=10)
        start = tk.Button(frame_buttons, text='开始办理',
                          fg='black', command=self.click_start_number)
        start.pack(side='left', padx=10, pady=10)
        finish = tk.Button(frame_buttons, text='完成', fg='green',
                           command=self.click_finish_number)
        finish.pack(side='left', padx=10, pady=10)
        frame_buttons.pack()

        frame_status = tk.Frame(root)
        self.status = tk.Label(frame_status, text='')
        self.status.pack(side='left')
        frame_status.pack()

        # always on top
        root.attributes('-topmost', 'true')

        # root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def send_info(self, mode, num):
        # mdoe: 'start', 'finish', 'pause', 'miss'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            info = ','.join([str(CUR_WINDOW_NAME), str(mode), str(num)])
            try:
                sock.connect((HOST, PORT))
            except:
                self.status['text'] = '无法连接到服务端！'
                return
            sock.sendall(bytes(info + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(4096), "utf-8")

            print("Sent:     {}".format(info))
            print("Received: {}".format(received))

            if mode in ['miss', 'finish']:
                # if len(numbers) <= 1:
                #     self.status['text'] = '暂无办理。'
                # else:
                if received:
                    # wait_num, numbers = received.split('|')
                    # numbers = numbers.split(',')
                    wait_num = received
                    self.cur_nubmer.insert(0, wait_num)
                    self.status['text'] = '正在等待{}号...'.format(wait_num)
                else:
                    self.status['text'] = '暂无办理。'

    def is_valid_num(self, string_to_check):
        # if not string_to_check:
        #     return False
        # for c in string_to_check:
        #     if c not in '0123456789':
        #         return False
        # return True
        try:
            str_to_int = int(string_to_check)
            return str_to_int in settings.NUMS
        except:
            return False

    def click_start_number(self):
        num = self.cur_nubmer.get().strip()
        if not self.is_valid_num(num):
            self.status['text'] = '输入号码无效！'
            self.cur_nubmer.delete(0, tk.END)
            return
        # self.cur_nubmer.delete(0, tk.END)
        self.status['text'] = '正在为{}号办理业务...'.format(num)
        self.send_info('start', num)

    def click_miss_number(self):
        num = self.cur_nubmer.get().strip()
        if not self.is_valid_num(num):
            self.status['text'] = '输入号码无效！'
            self.cur_nubmer.delete(0, tk.END)
            return
        self.cur_nubmer.delete(0, tk.END)
        self.status['text'] = '{}号已过号！'.format(num)
        self.send_info('miss', num)

    def click_finish_number(self):
        num = self.cur_nubmer.get().strip()
        if not self.is_valid_num(num):
            self.status['text'] = '输入号码无效！'
            self.cur_nubmer.delete(0, tk.END)
            return
        self.cur_nubmer.delete(0, tk.END)
        self.status['text'] = '{}号已完成！'.format(num)
        self.send_info('finish', num)

    # def on_closing(self):
    #     pass


root = tk.Tk()
root.title('排号系统')
app = QMS_Client(root)
root.mainloop()
