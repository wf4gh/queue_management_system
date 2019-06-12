import tkinter as tk
import socketserver
import threading

import settings

HOST = settings.SERVER_HOST
PORT = settings.SERVER_PORT


class QMS_Server:
    def __init__(self, root):
        self.root = root
        frame1 = tk.Frame(self.root)
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

    def gen_text(self, window_num, cur_num, type='doing'):
        if type == 'doing':
            text = '{}号窗口: 正在为{}号办理'.format(window_num, cur_num)
        else:
            text = '{}号窗口: 正在等待{}号...'.format(window_num, cur_num)
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

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(str(self.data, encoding='utf-8'))
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())


root = tk.Tk()
root.title('办理进度')
server = QMS_Server(root)
root.mainloop()
# server.listen_sock()
