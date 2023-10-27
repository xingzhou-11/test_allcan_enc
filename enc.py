import canopen

class allcan_enc:

    def __init__(self):
        pass

    def read_val(self, node: canopen.LocalNode):
        val = node.sdo[0x2001].raw
        return val