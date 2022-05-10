# 22973676, Adrian Bedford
# 22989775, Oliver Lynch

# Multiple invocation of actions, each actionset is sequential
# Store any action outputs, report action failures
# Networking, checksum (hashlib)

import re, sys, subprocess, socket

# Ensure python 3.10 and above
MIN_PYTHON = (3, 10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

sockets = []


def main():
    print("| Rakefile parser |----------------")
    path = "Rakefile"

    if len(sys.argv) > 1:
        path = sys.argv[1]

    with open(path, "r") as rf:
        rflines = rf.readlines()
        actionSets = []
        currentActionset = -1

        port = 0
        hosts = []

        for line in rflines:
            line = line.strip("\n")
            line = line.replace("    ", "\t")
            match line.split():
                case ["#", *args]:
                    print("=-=-= comment =-=-=")
                    continue
                case [actionSet] if line.endswith(":"):
                    print("=-=-= new actionset =-=-=")
                    currentActionset += 1
                    actionSets.append([])
                case ["PORT", "=", val]:
                    print("=-=-= set port {0} =-=-=".format(val))
                    port = val
                case ["HOSTS", "=", *args]:
                    print("=-=-= set hosts {0} =-=-=".format(args))
                    hosts = args
                case [*cmd] if line.startswith("\t\trequires"):
                    print("=-=-= file required {0} =-=-=".format(cmd))
                case [*cmd] if line.startswith("\tremote-"):
                    cmd = " ".join(cmd)
                    print("=-=-= run remote {0} =-=-=".format(cmd))
                    actionSets[currentActionset].append([cmd, True])
                case [*cmd] if line.startswith("\t"):
                    cmd = " ".join(cmd)
                    print("=-=-= run command {0} =-=-=".format(cmd))
                    actionSets[currentActionset].append([cmd, False])
                case _:
                    print(line)
                    pass

        print(actionSets)
        print("=========================")

        for actionSet in actionSets:
            execute(actionSet)


def execute(actionSet):
    for command in actionSet:
        if not command[1]:  # Run locally
            process = subprocess.run(
                command[0], shell=True, capture_output=True, text=True, timeout=15
            )  # unsafe
            # try:
            #     out, err = process.communicate(timeout=15)
            # except subprocess.TimeoutExpired: # process exceeded timeout
            #     process.kill()
            #     out, err = process.communicate()
            # print(out, " -|- ", err)

            if process.stdout:
                print(process.stdout.strip())
            if process.stderr:
                print(process.stderr.strip())

        else:  # Run on network
            pass


def networkInit(port, hosts):
    hostNames = []

    for host in hosts:
        hostName = host.split(":")

        if len(hostName) == 1:
            hostName.append(port)

        hostNames.append(tuple(hostName))

    for host in hostNames:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(host)
        sockets.append(s)

def networkSendString():
    pass


if __name__ == "__main__":
    main()

    for s in sockets:
        s.close()
