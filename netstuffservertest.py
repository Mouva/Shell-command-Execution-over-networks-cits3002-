import networkstuff as net
import time

socks = net.start_server()


def incomingPacket(packet):
    # print(packet.filename, packet.filesize, packet.offset, packet.data.decode("utf-8"))
    if packet.control:
        net.write_packet(packet)


try:
    while True:
        net.poll(incomingPacket)

        time.sleep(1)
        print(".")
except KeyboardInterrupt:
    for sock in socks:
        sock.close()
