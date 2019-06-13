import tkinter as tk
import socketserver
import threading
from time import sleep

# import settings
import configparser

config = configparser.ConfigParser()
config.read('Config.ini', encoding='utf-8')

HOST = config['CONFIG']['server_host']
PORT = int(config['CONFIG']['server_port'])
ORDER = int(config['CONFIG']['local_order'])
RANGE = config['CONFIG']['number_range'].split(',')
# print(HOST)
# HOST = settings.SERVER_HOST
# print(HOST)
# PORT = settings.SERVER_PORT


class QMS_Server:
    """Server side, show current working status with info received from client side(s) and allocate customers."""

    def __init__(self, root):
        self.root = root
        frame1 = tk.Frame(self.root)
        self.w1 = tk.Label(frame1, text=self.gen_text(1))#, bg='red')
        self.w1.pack(side='top', pady=5)
        self.w2 = tk.Label(frame1, text=self.gen_text(2))#, bg='green')
        self.w2.pack(side='top', pady=5, after=self.w1)
        self.w3 = tk.Label(frame1, text=self.gen_text(3))
        self.w3.pack(side='top', pady=5)
        self.w4 = tk.Label(frame1, text=self.gen_text(4))
        self.w4.pack(side='top', pady=5)
        # self.w5 = tk.Label(frame1, text=self.gen_text(5))
        # self.w5.pack(side='top',pady=5)
        frame1.pack(padx=30, pady=10)

        # always on top
        self.root.attributes('-topmost', 'true')

        # self.s_sock = socket.socket()
        # host = socket.gethostname()
        # port = 1611
        # self.s_sock.bind((host, port))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.socket_server_thread = threading.Thread(target=self.start_server)
        self.socket_server_thread.start()

    def start_server(self):
        # print('start_thread')
        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as self.server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            self.server.serve_forever()
            # self.server.shutdown()
        # print('end_thread')

    # def listen_sock(self):
    #     self.s_sock.listen(5)
    #     while True:
    #         c_sock, addr = self.s_sock.accept()
    #         print(addr)
    #         c_sock.send('info send from s_sock')
    #         c_sock.close()

    def gen_text(self, window_num, type='no_work', cur_num=0):
        if type == 'doing':
            text = '{}号窗口: 正在为{}号办理'.format(window_num, cur_num)
        elif type == 'waiting':
            text = '{}号窗口: 正在等待{}号'.format(window_num, cur_num)
        elif type == 'no_work':
            text = '{}号窗口：暂无办理'.format(window_num)
        return text

    def on_closing(self):
        # print(1)
        self.server.shutdown()
        # print(2)
        self.socket_server_thread.join()
        # print(3)
        self.root.destroy()

        # pass
        # self.s_sock.close()


class MyTCPHandler(socketserver.StreamRequestHandler):
    # def __init__(self, window_labels):
    #     self.window_labels = window_labels

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        recv_info = str(self.data, encoding='utf-8')
        print(recv_info)
        # Likewise, self.wfile is a file-like object used to write back

        window_idx = ORDER
        # window_idx = settings.CLIENT_ORDER.index(self.client_address[0])

        # print(window_idx)


        mode, polished_info, win_num, customer_num = self.info_parser(
            recv_info)
        labels[window_idx]['text'] = polished_info
        if mode in ['miss', 'finish']:
            # print('here!')
            # sleep(.5)
            # if len(numbers) <= 1:
            if not numbers:
                labels[window_idx]['text'] = '{}：暂无办理'.format(win_num)
                self.wfile.write(bytes('', 'utf-8'))
            else:
                if int(customer_num) in numbers:
                    numbers.remove(int(customer_num))
                # next_num = numbers[0]
                next_num = numbers.pop(0)
                labels[window_idx]['text'] = '{}：正在等待{}号办理'.format(
                    win_num, next_num)
                # print(numbers)
                # to the client
                byte_numbers = bytes(str(next_num), 'utf-8')
                # byte_numbers = bytes(str(next_num) + '|' + ','.join([str(n) for n in numbers]), 'utf-8')
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
root.geometry('270x150')
server = QMS_Server(root)

labels = [server.w1, server.w2, server.w3, server.w4]
numbers = list(range(int(RANGE[0]), int(RANGE[1])))
root.mainloop()
