from PIL import ImageTk, Image
import numpy as np
import math
import os
import sys
import time
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'robotiq'))
from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper

FIRST_POS  = [1.8401131629943848, -1.1269958776286622, 2.2122414747821253, -1.0343037408641358, 1.8012726306915283, -3.1195295492755335]
SCND_POS  = [1.8260459899902344, -1.5173147295466443, 2.0494936148272913, -0.5320155185512085, 1.7650651931762695, -3.1326821486102503]
THRD_POS = [0.7112540006637573, -1.4228464525989075, 2.2909279505359095, -0.8680674594691773, 0.6849308013916016, -3.144525114689962]
FRTH_POS = [0.7202740907669067, -1.219908670788147, 2.324162308369772, -1.0743021231940766, 0.7115388512611389, -3.1443727652179163]

def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)
    gripper.move(0,125,125)
    #joint_state = [1.678962230682373, -1.456998625104763, 1.185784165059225, -1.3145130437663575, -1.593665901814596, 0.21881437301635742]
    robot.move_joint_list(FIRST_POS, 0.25, 0.5, 0.02)
    print("moved to 1st position")
    
    gripper.move(140,125,125)
    time.sleep(1)
    joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    #joint_state = [0.5610477328300476, -1.1036332410625, 2.3208144346820276, -1.1481465560248871, -5.74299389520754, 3.142294406890869]
    gripper.move(140,125,125)
    robot.move_joint_list(SCND_POS, 0.25, 0.5, 0.02)
    print("moved to 2nd position")
    
    time.sleep(1)
    robot.move_joint_list(THRD_POS, 0.25, 0.5, 0.02)
    print("moved to 3rd position")
    
    gripper.move(140,125,125)
    time.sleep(1)
    joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    #joint_state = [0.5610477328300476, -1.1036332410625, 2.3208144346820276, -1.1481465560248871, -5.74299389520754, 3.142294406890869]
    robot.move_joint_list(FRTH_POS, 0.25, 0.5, 0.02)
    gripper.move(0,125,125)
    print("moved to 4th position")
    
    
def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)    
 

if __name__=="__main__":
     main()