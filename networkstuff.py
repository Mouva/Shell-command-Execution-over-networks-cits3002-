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
BLOCKING_TIME = 10


def sockets():
    return socks


class packet:
    def __init__(self, control, filename, filesize, offset, data, sock=None):
        self.control = int(control)
        self.filename = filename
        self.filesize = int(filesize)
        self.offset = int(offset)
        self.socket = sock

        if type(data) == str:
            self.data = data.encode("utf-8")
        elif type(data) == bytes:
            self.data = data

    def asBytes(self):
        datasize = [1, 64, 64, 64, DATA_SIZE]
        data = [
            int(self.control).to_bytes(1, "little"),
            self.filename.encode("utf-8"),
            int(self.filesize).to_bytes(64, "little"),
            int(self.offset).to_bytes(64, "little"),
            self.data,
        ]

        pack = b"\x01" * 7

        for size, param in zip(datasize, data):
            pack += slackfill(param, size)

        return pack

    def send(self, s=None):
        s = s or self.socket
        s.settimeout(BLOCKING_TIME)
        s.sendall(self.asBytes())

    @staticmethod
    def unpacket(pack, sock=None):
        control = int(pack[7])
        filename = pack[8:72].decode("utf-8").strip("\x00")
        filesize = int.from_bytes(pack[72:136].lstrip(b"\x00"), "little")
        offset = int.from_bytes(pack[136:200].lstrip(b"\x00"), "little")
        data = pack[
            200 : HEADER_SIZE + (filesize - offset)
        ]  # Trim any excess nulls from data

        return packet(control, filename, filesize, offset, data, sock)


class remoteProcess:
    def __init__(self, id, command):
        self.id = id
        self.command = command

        self.candidates = []

        self.query()

    def query(self):
        for sock in socks:
            pack = packet(0, "", self.id, 0, self.command)
            send(pack)

    def candidate(self, pack):
        self.candidates.append([pack.offset, pack.socket])

    def run(self):
        self.candidates.sort(key=lambda p: p[0])

        sock = self.candidates.pop(0)[1]

        packet(1, "", self.id, 0, self.command).send(sock)


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
    readqueue.append(b"")
    # readqueue.append(queue.Queue(maxsize=PACKET_SIZE * 1.5))

    # return socks


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
        readqueue.append(b"")

    # return socks


def poll(callback):

    # for sock in socks
    read, write, exception = select.select(socks, socks, [], 10)

    # print(read, write)

    for sock in read:
        si = socks.index(sock)
        # for pack in buffer(sock):
        #     callback(packet.unpacket(pack))
        # while not readqueue[sockindex].full():
        #     sock.setblocking(0)
        #     incoming = sock.recv(1)
        #     sock.setblocking(BLOCKING_TIME)
        #     if incoming:
        #         readqueue[sockindex].put(incoming)
        #     else:
        #         break

        # while readqueue[sockindex].qsize() >= PACKET_SIZE:
        #     print("BBBBCBBCBBCBBBCBBCBBCCCBBCBCBBBBC")
        #     if readqueue[sockindex].get() == b"\x01":
        #         pack = b"\x01"
        #         for byte in range(PACKET_SIZE - 1):
        #             pack += readqueue[sockindex].get()
        #         print("AAAAAAABABABABBdaddyBABBBBAAABBBAAAAA")
        #         callback(packet.unpacket(pack))

        readqueue[si] += sock.recv(PACKET_SIZE)

        while len(readqueue[si]) >= PACKET_SIZE:
            if b"\x01" in readqueue[si]:
                packStart = readqueue[si].index(b"\x01")

                if PACKET_SIZE + packStart <= len(readqueue[si]):
                    callback(
                        packet.unpacket(
                            readqueue[si][packStart : packStart + PACKET_SIZE], sock
                        )
                    )
                    readqueue[si] = readqueue[si][packStart + PACKET_SIZE :]
                else:
                    readqueue[si] += sock.recv(PACKET_SIZE)
            else:
                readqueue[si] = b""

    for sock in write:
        wq = writequeue[socks.index(sock)]
        while not wq.empty():

            pack = wq.get()
            pack.send(sock)


# def buffer(sock):
#     buf = sock.recv(PACKET_SIZE)
#     buffering = True
#     while buffering:
#         if b"\x01" in buf:
#             pos = buf.index(b"\x01" * 7)
#             if pos + PACKET_SIZE <= len(buf):
#                 yield buf[pos : pos + PACKET_SIZE]
#             else:
#                 more = sock.recv(PACKET_SIZE)
#                 if not more:
#                     buffering = False
#                 else:
#                     buf += more
#     if buf:
#         yield buf


def send(sock, packet):
    writequeue[socks.index(sock)].put(packet)
