#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Leds
    ("user_led", 0, Pins("AB8"),  IOStandard("LVCMOS15")),
    ("user_led", 1, Pins("AA8"),  IOStandard("LVCMOS15")),
    ("user_led", 2, Pins("AC9"),  IOStandard("LVCMOS15")),
    ("user_led", 3, Pins("AB9"),  IOStandard("LVCMOS15")),
    ("user_led", 4, Pins("AE26"), IOStandard("LVCMOS25")),
    ("user_led", 5, Pins("G19"),  IOStandard("LVCMOS25")),
    ("user_led", 6, Pins("E18"),  IOStandard("LVCMOS25")),
    ("user_led", 7, Pins("F16"),  IOStandard("LVCMOS25")),

    # Buttons
    ("user_btn", 0, Pins("G12"),  IOStandard("LVCMOS25")),    # center button
    ("user_btn", 1, Pins("AA12"), IOStandard("LVCMOS15")),    # up button
    ("user_btn", 2, Pins("AB12"), IOStandard("LVCMOS15")),    # down button
    ("user_btn", 3, Pins("AC6"),  IOStandard("LVCMOS15")),    # left button
    ("user_btn", 4, Pins("AG5"),  IOStandard("LVCMOS15")),    # right button

    ("clk156", 0,
        Subsignal("p", Pins("K28"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("K29"), IOStandard("LVDS_25"))
    ),

    ("cpu_reset", 0, Pins("AB7"), IOStandard("LVCMOS15"))
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk156"
    default_clk_period = 1e9/156e6

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7k325t-ffg900-2", _io, toolchain="vivado")

# Design -------------------------------------------------------------------------------------------

# Create our platform (fpga interface)
platform = Platform()

# Create our module (fpga description)
class Switches(Module):
    def __init__(self, platform):
        # synchronous assignments
        self.sync += []
        # combinatorial assignements
        for i in range(5):
            led = platform.request("user_led", i)
            btn = platform.request("user_btn", i)
            self.comb += led.eq(btn)

module = Switches(platform)

# Build --------------------------------------------------------------------------------------------

platform.build(module)

