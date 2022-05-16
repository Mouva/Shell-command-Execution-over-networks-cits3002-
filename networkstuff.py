# 22973676, Adrian Bedford
# 22989775, Oliver Lynch


# Header 193
# ----------------
# \x01
# \x01
# \x01
# \x01
# \x01
# \x01
# \x01
# Control 1
# Specifies packet type
# - 0 for command
# - 1 for file

# Filename 64
# Filesize 64
# Byte Offset 64

# Data, the rest

import socket, os, select, queue

socks = []
readqueue = []
writequeue = []
HEADER_SIZE = 7 + 1 + 64 + 64 + 64
PACKET_SIZE = 1024
FOOTER_SIZE = 0
DATA_SIZE = PACKET_SIZE - HEADER_SIZE - FOOTER_SIZE
DEFAULT_PORT = 6666


class packet:
    def __init__(self, control, filename, filesize, offset, data):
        self.control = int(control).to_bytes(1, "little")
        self.filename = filename.encode("utf-8")
        self.filesize = int(filesize).to_bytes(64, "little")
        self.offset = int(offset).to_bytes(64, "little")

        if type(data) == str:
            self.data = data.encode("utf-8")
        elif type(data) == bytes:
            self.data = data

    def asBytes(self):
        datasize = [1, 64, 64, 64, DATA_SIZE]
        data = [
            self.control,
            self.filename,
            self.filesize,
            self.offset,
            self.data,
        ]

        pack = b"\x01" * 7

        for size, param in zip(datasize, data):
            pack += slackfill(param, size)

        return pack

    def send(self, s):
        s.settimeout(30)
        s.sendall(self.asBytes())

    @staticmethod
    def unpacket(pack):
        filesize = int.from_bytes(pack[72:136], "little")
        offset = int.from_bytes(pack[137:201], "little")

        return packet(
            pack[7],
            pack[8:72].decode("utf-8").strip("\x00"),
            filesize,
            offset,
            pack[
                202 : HEADER_SIZE + (filesize - offset) - 1
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


def start_server(host="", port=DEFAULT_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    c, address = s.accept()

    socks.append(c)
    writequeue.append(queue.Queue())

    return socks


def start_client(hosts, port=DEFAULT_PORT):
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
        writequeue.append(queue.Queue())
        # readqueue.append(queue.Queue(maxsize=(PACKET_SIZE * 2) - 1))

    return socks


def poll(callback):

    # for sock in socks
    read, write, exception = select.select(socks, socks, [], 10)

    # print(read, write)

    for sock in read:
        for pack in buffer(sock):
            callback(packet.unpacket(pack))

    for sock in write:
        wq = writequeue[socks.index(sock)]
        while not wq.empty():

            pack = wq.get()
            pack.send(sock)


def buffer(sock):
    buf = sock.recv(PACKET_SIZE)
    buffering = True
    while buffering:
        if b"\x01" in buf:
            pos = buf.index(b"\x01" * 7)
            if pos + PACKET_SIZE <= len(buf):
                yield buf[pos : pos + PACKET_SIZE]
            else:
                more = sock.recv(PACKET_SIZE)
                if not more:
                    buffering = False
                else:
                    buf += more
    if buf:
        yield buf


def send(sock, packet):
    writequeue[socks.index(sock)].put(packet)
