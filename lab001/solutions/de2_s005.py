#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.altera import AlteraPlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led",  0, Pins("G19"), IOStandard("3.3-V LVTTL")),
    ("user_led",  1, Pins("F19"), IOStandard("3.3-V LVTTL")),
    ("user_led",  2, Pins("E19"), IOStandard("3.3-V LVTTL")),
    ("user_led",  3, Pins("F21"), IOStandard("3.3-V LVTTL")),

    ("user_sw",  0, Pins("AB28"), IOStandard("3.3-V LVTTL")),
    
    ("user_btn", 0, Pins("M23"), IOStandard("3.3-V LVTTL")),

    ("clk50", 0, Pins("Y2"), IOStandard("3.3-V LVTTL"))

    #("cpu_reset", 0, Pins("C12"), IOStandard("LVCMOS33")),

    #("user_rgb_led_r", 0, Pins("N16"), IOStandard("LVCMOS33")),
    #("user_rgb_led_g", 0, Pins("R11"), IOStandard("LVCMOS33")),
    #("user_rgb_led_b", 0, Pins("G14"), IOStandard("LVCMOS33"))
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


class RGBBlink(Module):
    def __init__(self, platform):
        # submodules
        blink_r = Blink(1, 100e6, platform.request("user_led",1))
        blink_g = Blink(2, 100e6, platform.request("user_led",2))
        blink_b = Blink(4, 100e6, platform.request("user_led",3))
        self.submodules += blink_r, blink_g, blink_b

module = RGBBlink(platform)

# Build --------------------------------------------------------------------------------------------

platform.build(module)

