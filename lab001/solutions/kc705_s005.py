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
        blink_r = Blink(1, 156e6, platform.request("user_led",0))
        blink_g = Blink(2, 156e6, platform.request("user_led",1))
        blink_b = Blink(4, 156e6, platform.request("user_led",2))
        self.submodules += blink_r, blink_g, blink_b

module = RGBBlink(platform)

# Build --------------------------------------------------------------------------------------------

platform.build(module)

