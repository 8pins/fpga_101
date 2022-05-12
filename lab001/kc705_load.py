#!/usr/bin/env python3

import os

# if you have djtgcfg installed, run this

os.system("djtgcfg prog -d JtagSmt1 -i 0 -f ./solutions/build/top.bit")

# if you have openocd installed, run this
# from litex.build.openocd import OpenOCD
# from litex.soc.integration.builder import *
