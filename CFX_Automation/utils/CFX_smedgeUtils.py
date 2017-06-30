import os, sys, subprocess
import CFX_utils

projConfig = CFX_utils.getConfig('proj')

rootKey = "win"
if sys.platform == "linux" or sys.platform == "linux2":
    rootKey = "linux"
elif sys.platform == "darwin":
    # MAC OS X
    rootKey = "darwin"

SmedgeSubmitCommand = projConfig['smedge'][rootKey]
