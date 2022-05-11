# 22973676, Adrian Bedford
# 22989775, Oliver Lynch


# Header 193
# ----------------
# Control 1
# Filename 64
# Filesize 64
# Byte Offset 64

# Data, the rest


import socket, os

socks = []
HEADER_SIZE = 193
PACKET_SIZE = 1024
DATA_SIZE = PACKET_SIZE - HEADER_SIZE


class packet:
    def __init__(self, control, filename, filesize, offset, data):
        self.control = int(control).to_bytes(1, "little")  # 0
        self.filename = filename.encode("utf-8")
        self.filesize = int(filesize).to_bytes(64, "little")
        self.offset = int(offset).to_bytes(64, "little")

        self.data = bytes(data)

    def asBytes(self):
        datasize = [1, 64, 64, 64, DATA_SIZE]
        data = [self.control, self.filename, self.filesize, self.offset, self.data]

        pack = b""

        for size, param in zip(datasize, data):
            pack += slackfill(param, size)

        return pack

    def send(self, s):
        pass

    @staticmethod
    def unpacket(pack):
        filesize = int.from_bytes(pack[65:129], "little")
        offset = int.from_bytes(pack[129:193], "little")

        print()


        return (
            pack[0],
            pack[1:65].decode("utf-8").strip("\x00"),
            filesize,
            offset,
            pack[193:HEADER_SIZE + (filesize - offset)],
        )


# The enpackulator
def enpacket(filename):
    packets = []

    with open(filename, "rb") as f:
        # f.seek(n,0) # Ensure at start of file
        filesize = os.path.getsize(filename)
        curpos = 0

        while pack := f.read(DATA_SIZE):
            packets.append(packet(1, filename, filesize, curpos, pack))
            curpos = f.tell()

    return packets


def stripping(packets):
    pass


def combine(packets):
    pass


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
        s.connect(host)
        socks.append(s)
