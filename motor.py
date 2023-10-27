import canopen

class flow_motor:

    def __init__(self):
        pass

    def position_mode_run(
            self, 
            node: canopen.LocalNode, 
            position: int, 
            speed: int, 
            acceleration: int, 
            deceleration: int):
        """_summary_

        Args:
            node (canopen.LocalNode): motor node
            position (int): target position
            speed (int): target speed
            acceleration (int): _description_
            deceleration (int): _description_
        """
        node.sdo.download(0x6060, 0, b'\x01')
        node.sdo.download(0x607A, 0, position.to_bytes(4, byteorder='little'))
        node.sdo.download(0x6081, 0, speed.to_bytes(4, byteorder='little'))
        node.sdo.download(0x6083, 0, acceleration.to_bytes(4, byteorder='little'))
        node.sdo.download(0x6084, 0, deceleration.to_bytes(4, byteorder='little'))
        node.sdo.download(0x6040, 0, b'\x06\x00')
        node.sdo.download(0x6040, 0, b'\x0F\x00')
        node.sdo.download(0x6040, 0, b'\x3F\x00')

    
    def read_position_val(self, node: canopen.LocalNode):
        val = node.sdo[0x6064].raw
        return val
    
    def check_pos_arrival(self, node: canopen.LocalNode):
        val = 0
        val = node.sdo[0x6041].raw & 0x400
        # val += node.sdo[0x6040].raw & 0x100
        return val
        