import networkstuff as net
import time

socks = net.start_server()


def incomingPacket(packet):
    print(packet.filename, packet.data)


try:
    while True:
        net.poll(incomingPacket)

        time.sleep(1)
        print(".")
except KeyboardInterrupt:
    for sock in socks:
        sock.close()
