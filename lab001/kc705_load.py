#!/usr/bin/env python3

import os

# if you have djtgcfg installed, run this

os.system("djtgcfg prog -d kc705 -i 0 -f ./build/top.bit")

# if you have openocd installed, run this
# from litex.build.openocd import OpenOCD
# from litex.soc.integration.builder import *
