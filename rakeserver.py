# 22973676, Adrian Bedford
# 22989775, Oliver Lynch

import sys, subprocess
import networkstuff as net

# Ensure python 3.10 and above
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def main():
    HOST = ''
    PORT = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    c, address = s.accept()

    print("<==== Successfully connected to", address, "====>")

    while True:
        rData = c.recv(4096).decode()
        if rData:
            print(rData)
        if rData:
            c.send(bytes(chr(6), 'utf_8'))
            process = subprocess.run(rData, shell=True, capture_output=True, text=True, timeout=15)
            if process.stdout:
                print(process.stdout.strip())
                c.send(process.stdout.strip()).encode()
            if process.stderr:
                print(process.stderr.strip())
                c.send(process.stdout.strip()).encode()
            break
        
    print("<==== End transmission ====>")
    c.close()


if __name__ == "__main__":
    main()
