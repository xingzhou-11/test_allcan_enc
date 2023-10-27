#!/usr/bin/python3
import time
import canopen
import argparse
from enc import allcan_enc
from motor import flow_motor

def main(target_position, target_speed):
    allcanenc = allcan_enc()
    flowmotor = flow_motor()
    
    network = canopen.Network()
    network.connect(channel='can0', bustype='socketcan')

    enc_node = network.add_node(13, 'allcan_q.eds')
    motor_node = network.add_node(2, 'flowservo.eds')

    enc_node.sdo.RESPONSE_TIMEOUT = 1
    motor_node.sdo.RESPONSE_TIMEOUT = 1

    network.nmt.state = 'OPERATIONAL'
    
    allcanenc.read_val(enc_node)
    flowmotor.read_position_val(motor_node)
    
    # --------------------------------------------------------------------------------------------------
    print("initial value")
    flow_motor_position = flowmotor.read_position_val(motor_node)
    flow_motor_position = flow_motor_position * 0.4 # Convert motor subdivision into encoder subdivision
    
    print(f'allcan-enc position: {allcanenc.read_val(enc_node)}')
    print(f'flow-motor position: {flow_motor_position}') 
    # -------------------------------------------------------------------------------------------------- 

    flowmotor.position_mode_run(motor_node, target_position, target_speed, 35000, 35000)

    # wait motor stop
    while (flowmotor.check_pos_arrival(motor_node) != 1024): # bit10 置1 为位置到达 ==> 1024
        time.sleep(1)
    
    # --------------------------------------------------------------------------------------------------
    print("The first trip is over")
    flow_motor_position = flowmotor.read_position_val(motor_node)
    flow_motor_position = flow_motor_position * 0.4 # Convert motor subdivision into encoder subdivision
    
    print(f'allcan-enc position: {allcanenc.read_val(enc_node)}')
    print(f'flow-motor position: {flow_motor_position}')
    # --------------------------------------------------------------------------------------------------

    flowmotor.position_mode_run(motor_node, 0, target_speed, 35000, 35000)

    while (flowmotor.check_pos_arrival(motor_node) != 1024):
        time.sleep(1)

    # --------------------------------------------------------------------------------------------------
    print("The second trip is over") 
    flow_motor_position = flow_motor.read_position_val(motor_node)
    flow_motor_position = flow_motor_position * 0.4 # Convert motor subdivision into encoder subdivision
    
    print(f'allcan-enc position: {allcanenc.read_val(enc_node)}')
    print(f'flow-motor position: {flow_motor_position}')
    # --------------------------------------------------------------------------------------------------

    network.disconnect()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='allcan-enc test.')
    parser.add_argument("target_position", help="target position (rev).", type = int)
    parser.add_argument("target_speed", help="target speed (m/s).", type = int)

    args = parser.parse_args()

    target_position = args.target_position * 10000 # Revolutions * subdivide
    target_speed = args.target_speed * 10000 # m/s * subdivide
    
    main(target_position, target_speed)

