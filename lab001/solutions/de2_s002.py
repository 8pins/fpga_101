#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.altera import AlteraPlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led",  0, Pins("G19"), IOStandard("3.3-V LVTTL")),

    ("user_sw",  0, Pins("AB28"), IOStandard("3.3-V LVTTL")),

    ("user_btn", 0, Pins("M23"), IOStandard("3.3-V LVTTL")),

    ("clk50", 0, Pins("Y2"), IOStandard("3.3-V LVTTL"))

]

# Platform -----------------------------------------------------------------------------------------

class Platform(AlteraPlatform):
    default_clk_name   = "clk50"        
    default_clk_period = 1e9/50e6       # clock is 50 MHz

    def __init__(self, toolchain="quartus"):
        AlteraPlatform.__init__(self, "EP4CE115F29C7", _io, toolchain=toolchain)
# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)
platform = Platform()

# Create our module (fpga description)
class Blink(Module):
    def __init__(self, blink_freq, sys_clk_freq, led):
        counter = Signal(32)
        # synchronous assignments
        self.sync += [
            counter.eq(counter + 1),
            If(counter == int((sys_clk_freq/blink_freq)/2 - 1),
                counter.eq(0),
                led.eq(~led)
            )
        ]
        # combinatorial assignements
        self.comb += []

module = Blink(1, 50e6, platform.request("user_led"))
# create module Blink with blink_freq = 1 Hz, sys_clk_freq = 50 Hz
# Build --------------------------------------------------------------------------------------------

platform.build(module)

