#!/usr/bin/env python3

from migen import *

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led", 0, Pins("AB8"),  IOStandard("LVCMOS15")),

    ("user_dip_btn", 0, Pins("Y29"),  IOStandard("LVCMOS25")),

    ("user_btn_c", 0, Pins("G12"),  IOStandard("LVCMOS25")),

    ("clk200", 0,
        Subsignal("p", Pins("AD12"), IOStandard("LVDS")),
        Subsignal("n", Pins("AD11"), IOStandard("LVDS"))
    ),

    ("clk156", 0,
        Subsignal("p", Pins("K28"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("K29"), IOStandard("LVDS_25"))
    ),

    ("cpu_reset", 0, Pins("AB7"), IOStandard("LVCMOS15"))
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk156"
    default_clk_period = 1e9/156.5e6

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7k325t-ffg900-2", _io, toolchain="vivado")

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

module = Blink(1, 156.5e6, platform.request("user_led"))

# Build --------------------------------------------------------------------------------------------

platform.build(module)

