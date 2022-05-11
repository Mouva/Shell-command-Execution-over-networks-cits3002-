# 22973676, Adrian Bedford
# 22989775, Oliver Lynch

# 4096

# Filename 64
# Filesize 64
# Packet Number 32
# Packet Total 32

# Data 3840

# Checksum 64

import socket, subprocess

socks = []

class packet:
    def __init__(self, filename):
        self.filename = filename.encode('utf-8')
        self.filesize = 0
        self.packetNumber = 0
        self.packetTotal = 0

        self.data = b''

        self.check = b''        

    def asBytes(self):
        return self.filename + bytes(self.filesize) + bytes(self.filesize) + bytes(self.packetNumber) + self.data

    def send(self, s):
        pass

    def checksum(self):
        pack = sum(bytearray(self.asBytes()))
        return pack - (1 << 8) if pack & (1 << (8 - 1)) else pack

    def validate(self, noBitches):
        return sum(bytearray(self.asBytes() + bytes(noBitches)))


def start_server(host='', port=6666):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    c, address = s.accept()


def start_client(hosts, port=6666):
    hostNames = []

    for host in hosts:
        hostName = host.split(":")

        if len(hostName) == 1:
            hostName.append(port)

        hostNames.append(tuple(hostName))


    for host in hostNames:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(host)
        socks.append(s)
