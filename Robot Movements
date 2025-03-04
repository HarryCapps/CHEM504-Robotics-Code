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
FIRST_POS = [1.9598381519317627, -1.8197394810118617, 2.0655067602740687, -0.2610810560039063, 1.9489684104919434, 3.1007790565490723] #Home position
SCND_POS  = [1.8568476438522339, -1.0523559612086792, 2.228867832814352, -1.175378904943802, 1.8485941886901855, 3.121866464614868] #Going to Sample vial position
THRD_POS  = [1.8578236103057861, -1.447265812461712, 2.110725227986471, -0.6615637105754395, 1.847927212715149, 3.124692440032959] #Up + vertical after pick position
FRTH_POS = [1.1681103706359863, -2.01121248821401, 2.5829289595233362, -0.5724046987346192, 1.1567866802215576, 3.1245429515838623] #Position above stirrer
FIFTH_POS = [1.1671242713928223, -1.794520994225973, 2.697186533604757, -0.9027928870967408, 1.1570861339569092, 3.123086452484131] #Position in stirrer
SIXTH_POS = [1.418738842010498, -1.2759456199458619, 1.2870314756976526, 1.557830734843872, 1.5609979629516602, 2.964608669281006] # Gripper goes vertical
SVNTH_POS = [1.412574291229248, -1.2245715421489258, 1.5707538763629358, 1.2227379518696289, 1.5618265867233276, 2.960045576095581] # Gripper goes back down to collect sample vial



def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper=RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)
    gripper.move(0,125,125) #Gripper fully opened
    #joint_state = [1.678962230682373, -1.456998625104763, 1.185784165059225, -1.3145130437663575, -1.593665901814596, 0.21881437301635742]
    robot.move_joint_list(FIRST_POS, 0.25, 0.5, 0.02)
    print("moved to 1st position")
    
    time.sleep(1)
    gripper.move(0,125,125)
    joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    #joint_state = [0.5610477328300476, -1.1036332410625, 2.3208144346820276, -1.1481465560248871, -5.74299389520754, 3.142294406890869]
    gripper.move(0,125,125)
    robot.move_joint_list(SCND_POS, 0.25, 0.5, 0.02)
    print("moved to 2nd position")
    gripper.move(140,125,125) #sample being held
    
    time.sleep(1)
    robot.move_joint_list(THRD_POS, 0.25, 0.5, 0.02)
    print("moved to 3rd position")
    gripper.move(140,125,125) #sample being held
    
    gripper.move(140,125,125) #sample being held
    time.sleep(1)
    joint_state = degreestorad([-5.61,-83.95,112.70,-119.79,-90.07,-5.48])
    #joint_state = [0.5610477328300476, -1.1036332410625, 2.3208144346820276, -1.1481465560248871, -5.74299389520754, 3.142294406890869]
    robot.move_joint_list(FRTH_POS, 0.25, 0.5, 0.02)
    gripper.move(140,125,125) #sample being held
    print("moved to 4th position")
     
    time.sleep(1)
    robot.move_joint_list(FIFTH_POS, 0.1, 0.2, 0.02) #slowed down the movement and speed of robot for this small intricate movement
    gripper.move(0,125,125)
    print("Moved to 5th Position")
    
    time.sleep(3)
    robot.move_joint_list(FRTH_POS, 0.25, 0.5, 0.02)
    gripper.move(0,125,125) # return back to 4th position
    print("moved to 4th position")
    
    time.sleep(1)
    gripper.move(0,125,125)
    robot.move_joint_list(SIXTH_POS, 0.35, 0.5, 0.02) #gripper moved vertical 
    print("Moved to 6th Position")
    
    time.sleep(30) #keeps robot in position for 30 seconds to allow stir time
    robot.move_joint_list(SVNTH_POS, 0.25, 0.5, 0.02)
    gripper.move(140, 125, 125)
    print("Moved to 7th position")
    
    time.sleep(1)
    gripper.move(140,125,125)
    robot.move_joint_list(SIXTH_POS, 0.35, 0.5, 0.02) #gripper moved vertical 
    print("Moved to 6th Position")
    
#     time.sleep(30) 
#     robot.move_joint_list(FRTH_POS, 0.25, 0.5, 0.02)
#     print("Moved back to 4th position")

#     time.sleep(1) #moves the vial above the white background
#     robot.move_joint_list(SVNTH_POS, 0.7, 0.5, 0.02)
#     print("Moved to 7th position")
    
#     time.sleep(1) #moves the vial in front of the white background
#     robot.move_joint_list(EIGHT_POS, 0.8, 0.5, 0.02)
#     print("Moved to 8th position")
    
def degreestorad(list):
     for i in range(6):
          list[i]=list[i]*(math.pi/180)
     return(list)    
 

if __name__=="__main__":
     main()
