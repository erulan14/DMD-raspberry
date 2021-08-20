class PinLayout(object):
    OE = 24
    A = 39
    B = 40
    STROBE = 37  # [SLCK] [LATCH] [STROBE]

    def __init__(self, a, b, latch, oe):
        self.A = a
        self.B = b
        self.STROBE = latch
        self.OE = oe
