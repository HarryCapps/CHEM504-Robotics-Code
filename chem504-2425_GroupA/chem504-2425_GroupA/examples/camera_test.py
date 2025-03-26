import time
import math
import os
import sys
from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper

import cv2
import numpy as np
import time
import csv
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os


CSV_FILE_PATH = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/blue_pixel_data.csv")

# Initialize webcam
cam = cv2.VideoCapture(0)

# Create a window to display the feed
cv2.namedWindow("test")

# Thresholds
blue_pixel_threshold = 0  # Minimum blue pixels required to consider it "blue"
reaction_threshold = 50  # Total required blue pixels for successful detection
blue_pixel_below_threshold_duration = 5  # Number of seconds below threshold before stopping

# Track blue pixel count over time
blue_pixel_counts = []
times = []

# Define Region of Interest (ROI)
roi_x, roi_y, roi_w, roi_h = 200, 150, 260, 280 


# Track time
start_time = time.time()
last_logged_time = -1
below_threshold_counter = 3  # Track how long the reaction is not blue

try:
    while True:
        # Check if ESC key is pressed
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # ESC key
            print("Escape hit, closing...")
            break

        # Capture frame
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Crop the frame to the ROI
        roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Extract color channels
        blue_channel = roi_frame[:, :, 0]
        green_channel = roi_frame[:, :, 1]
        red_channel = roi_frame[:, :, 2]

        # Define blue mask
        blue_mask = (blue_channel > 150) & (green_channel < 100) & (red_channel < 100)

        # Count blue pixels
        blue_pixel_count = np.count_nonzero(blue_mask)
        
        # Track elapsed seconds
        elapsed_seconds = int(time.time() - start_time)

      
        # Draw ROI on frame
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
        cv2.imshow("test", frame)   
        
        # Convert mask to displayable format
        blue_mask_display = cv2.merge([blue_mask.astype(np.uint8) * 255] * 3)
        cv2.imshow("Blue Mask", blue_mask_display)       

        
        
        started = False 
        # while not started:
        #     if blue_pixel_count > 0:
        #         elapsed_seconds = 0
        #         started = True
        #     elif elapsed_seconds > 20:
        #         break
        #     else:
        #         print(f"Waiting {elapsed_seconds}")

        # Only log data once per second
        if elapsed_seconds > last_logged_time:
            last_logged_time = elapsed_seconds  # Update last log time
            if blue_pixel_count > 0 :
                if started:
                    blue_pixel_counts.append((elapsed_seconds, blue_pixel_count))
                    print(f"Time: {elapsed_seconds}s, Blue Pixels: {blue_pixel_count}")
                else: 
                    print("Lets get this party stared! ")
                    started = True
            elif not started : 
                print(f"Time waiting : {elapsed_seconds}s, Blue Pixels: {blue_pixel_count}")
            else :
                print("i think im done  ???")
            

        # Check if the reaction is still blue
        if blue_pixel_count >= blue_pixel_threshold:
            below_threshold_counter = 0  # Reset counter if blue is detected
        else:
            below_threshold_counter += 1
            print(f"Blue below threshold for {below_threshold_counter} seconds.")

            # Stop the loop if blue is gone for the set duration
            if below_threshold_counter >= blue_pixel_below_threshold_duration:
                print("The reaction is no longer blue. Stopping.")
                break

    

      

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Release webcam
    cam.release()
    cv2.destroyAllWindows()

    # Save CSV file
    try:
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time (Seconds)", "Blue Pixel Count"])
            writer.writerows(blue_pixel_counts)
        print(f"Data successfully saved in: {CSV_FILE_PATH}")
    except Exception as e:
        print(f"Error while saving CSV file: {e}")

    # Check if enough blue was detected
    if sum(count for _, count in blue_pixel_counts) >= reaction_threshold:
        print("Sample vial is blue")
    else:
        print("Sample vial did not reach the blue threshold")
