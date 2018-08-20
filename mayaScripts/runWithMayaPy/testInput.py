import sys
from pymel.core import *


def main(mayaFile):
    print mayaFile

if __name__=='__main__':
    mayaFile = sys.argv[-1]
    main(mayaFile)
