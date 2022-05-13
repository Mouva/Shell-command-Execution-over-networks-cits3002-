# 22973676, Adrian Bedford
# 22989775, Oliver Lynch


# Header 193
# ----------------
# \x01
# Control 1
# Specifies packet type
# - 0 for command
# - 1 for file

# Filename 64
# Filesize 64
# Byte Offset 64

# Data, the rest

# \x04

import socket, os

socks = []
HEADER_SIZE = 64 + 64 + 64 + 2
PACKET_SIZE = 1024
FOOTER_SIZE = 1
DATA_SIZE = PACKET_SIZE - HEADER_SIZE - FOOTER_SIZE


class packet:
    def __init__(self, control, filename, filesize, offset, data):
        self.control = int(control).to_bytes(1, "little")
        self.filename = filename.encode("utf-8")
        self.filesize = int(filesize).to_bytes(64, "little")
        self.offset = int(offset).to_bytes(64, "little")

        self.data = bytes(data)

    def asBytes(self):
        datasize = [1, 1, 64, 64, 64, DATA_SIZE, 1]
        data = [
            chr(1),
            self.control,
            self.filename,
            self.filesize,
            self.offset,
            self.data,
            chr(1),
        ]

        pack = b""

        for size, param in zip(datasize, data):
            pack += slackfill(param, size)

        return pack

    def send(self, s):
        pass

    @staticmethod
    def unpacket(pack):
        filesize = int.from_bytes(pack[66:130], "little")
        offset = int.from_bytes(pack[130:194], "little")

        print()

        return (
            pack[1],
            pack[2:66].decode("utf-8").strip("\x00"),
            filesize,
            offset,
            pack[
                194 : HEADER_SIZE + (filesize - offset) - 1
            ],  # Trim any excess nulls from data
        )


# The enpackulator (Read a file into packet objects)
def enpacket(filename):
    packets = []  # Keeps whole file in memory... could be more efficient

    with open(filename, "rb") as f:
        # f.seek(n,0) # Ensure at start of file
        filesize = os.path.getsize(filename)
        curpos = 0

        while pack := f.read(DATA_SIZE):
            packets.append(packet(1, filename, filesize, curpos, pack))
            curpos = f.tell()

    return packets


# Write a packet to a file on disc
def write_packet(pack):
    try:  # touch file and reserve space
        with open(pack.filename, "xb") as x:
            x.write(bytes(pack.filesize))
            x.close()
    except FileExistsError:
        pass

    with open(pack.filename, "r+b") as f:
        f.seek(pack.offset, 0)
        f.write(pack.data)


# Pad bytes with NULL to achieve target length
def slackfill(data, target):
    return data + bytes(target - len(data))


def start_server(host="", port=6666):
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
        s.settimeout(10)
        s.connect(host)
        socks.append(s)


def poll(callback):
    for sock in socks:
        while True:
            recv = packet.unpacket(sock.recv(PACKET_SIZE))

        callback(recv)
