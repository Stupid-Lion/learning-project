import socket
def func():
    in_addr = socket.gethostbyname(socket.gethostname())
    return in_addr

for i in range(3):
    ip = func()
    print(ip)
