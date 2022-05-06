#22973676, Adrian Bedford
#22989775, Oliver Lynch

import re
import sys
import subprocess

# Ensure python 3.10 and above
MIN_PYTHON = (3,10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

def main():
    print("| Rakefile parser |----------------")
    with open('Rakefile', 'r') as rf:
        rflines = rf.readlines()
        actionSets = {}
        currentActionset = ""

        port = 0
        hosts = []

        for line in rflines:
            line=line.replace("    ", "~ ").strip("\n")
            match line.split():
                case ["#", *args]:
                    print("=-=-= comment =-=-=")
                    continue
                case [actionSet] if line.endswith(":"):
                    print("=-=-= new actionset =-=-=")
                    actionSets[actionSet[:-1]] = []
                    currentActionset = actionSet[:-1]
                case ["PORT", "=", val]:
                    print("=-=-= set port {0} =-=-=".format(val))
                    port = val
                case ["HOSTS", "=", *args]:
                    print("=-=-= set hosts {0} =-=-=".format(args))
                    hosts = args
                case ["~", *cmd]:
                    cmd = " ".join(cmd)
                    print("=-=-= run command {0} =-=-=".format(cmd))
                    actionSets[currentActionset].append(cmd)
                case ["\tremote", *cmd]:
                    print("=-=-= run remote {0} =-=-=".format(cmd))
                case _:
                    print(line)
                    pass

        print(actionSets)

        execute(actionSets["actionset1"])

def execute(actionSet):
    for command in actionSet:
        process = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15) # unsafe
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


if __name__ == "__main__":
    main()
