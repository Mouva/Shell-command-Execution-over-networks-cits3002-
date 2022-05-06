#22973676, Adrian Bedford
#22989775, Oliver Lynch

import re
import sys

# Ensure python 3.10 and above
MIN_PYTHON = (3,10)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

def main():
    print("suck us (Adrian bedford 22973676 and also oliver lynch 22989775), daddy")
    with open('Rakefile', 'r') as rf:
        rflines = rf.readlines()

        for line in rflines:
            match line.split():
                case [var, "=", val]




if __name__ == "__main__":
    main()