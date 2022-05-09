# 22973676, Adrian Bedford
# 22989775, Oliver Lynch
#

import re, sys, subprocess, socket

# Ensure python 3.10 and above
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def main():
    HOST = "127.0.0.1"
    PORT = 6969

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"<====Connected succesfully to {addr}=====>")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


if __name__ == "__main__":
    main()
