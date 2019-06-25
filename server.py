import tkinter as tk
import socketserver
import threading
from time import sleep
from tkinter import font

# import settings
import configparser

config = configparser.ConfigParser()
config.read('Config.ini', encoding='utf-8-sig')
# config.read('Config.ini', encoding='utf-8')

HOST = config['CONFIG']['server_host']
PORT = int(config['CONFIG']['server_port'])
CLIENT_HOSTS = config['CONFIG']['client_host'].split(',')
RANGE = config['CONFIG']['number_range'].split(',')
numbers = list(range(int(RANGE[0]), int(RANGE[1]) + 1))
CLIENT_COUNT = int(config['CONFIG']['client_count'])
WIN_ALPHA = float(config['CONFIG']['server_win_alpha'])

class QMS_Server:
    """Server side, show current working status with info received from client side(s) and allocate customers."""

    def __init__(self, root, client_count=5):
        self.root = root
        frame1 = tk.Frame(self.root)
        self.labels = []
        ft = font.Font(size=20, weight=tk.font.BOLD)
        for i in range(client_count):
            l = tk.Label(frame1, text='{}号窗口：暂无办理'.format(i + 1), font=ft)
            l.pack(side='top', pady=5)
            self.labels.append(l)
        frame1.pack(padx=20, pady=10)

        # always on top
        self.root.attributes('-topmost', 'true')

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.socket_server_thread = threading.Thread(target=self.start_server)
        self.socket_server_thread.start()

    def start_server(self):
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as self.server:
            self.server.serve_forever()

    def on_closing(self):
        try:
            self.server.shutdown()
        except:
            print('fail shutdown self.server')
        self.socket_server_thread.join()
        self.root.destroy()


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        recv_info = str(self.data, encoding='utf-8')
        print(recv_info)

        mode, polished_info, win_num, customer_num = self.info_parser(
            recv_info)
        # print(ORDER)
        order = CLIENT_HOSTS.index(self.client_address[0])
        labels[order]['text'] = polished_info
        if mode in ['miss', 'finish']:
            if not numbers:
                labels[order]['text'] = '{}：暂无办理'.format(win_num)
                self.wfile.write(bytes('', 'utf-8'))
            else:
                if int(customer_num) in numbers:
                    numbers.remove(int(customer_num))
                next_num = numbers.pop(0)
                labels[order]['text'] = '{}：正在等待{}号办理'.format(
                    win_num, next_num)
                byte_numbers = bytes(str(next_num), 'utf-8')
                self.wfile.write(byte_numbers)
        elif mode == 'start':
            if int(customer_num) in numbers:
                numbers.remove(int(customer_num))
            self.wfile.write(bytes('', 'utf-8'))

    def info_parser(self, info):
        win_num, mode, customer_num = info.split(',')
        polished = ''
        if mode == 'start':
            polished = '{}：正在为{}号办理'.format(win_num, customer_num)
        elif mode == 'miss':
            polished = '{}：{}号已过号'.format(win_num, customer_num)
        elif mode == 'finish':
            polished = '{}：{}号已完成'.format(win_num, customer_num)
        return mode, polished, win_num, customer_num


root = tk.Tk()
root.title('办理进度')
root.geometry('500x200')
root.attributes('-alpha', WIN_ALPHA)
# root.overrideredirect(1)
server = QMS_Server(root, CLIENT_COUNT)
labels = server.labels
root.mainloop()
