import time
import math
import os
import sys
from utils.UR_Functions import URfunctions as URControl
from robotiq.robotiq_gripper import RobotiqGripper
import cv2
import numpy as np
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Robot position constants
ROBOT_POSITIONS = {
    "home": [1.9598381519317627, -1.8197394810118617, 2.0655067602740687, -0.2610810560039063, 1.9489684104919434, 3.1007790565490723],
    "sample_vial": [1.8568476438522339, -1.0523559612086792, 2.228867832814352, -1.175378904943802, 1.8485941886901855, 3.121866464614868],
    "up_vertical": [1.8578236103057861, -1.447265812461712, 2.110725227986471, -0.6615637105754395, 1.847927212715149, 3.124692440032959],
    "above_stirrer": [1.1681103706359863, -2.01121248821401, 2.5829289595233362, -0.5724046987346192, 1.1567866802215576, 3.1245429515838623],
    "in_stirrer": [1.1671242713928223, -1.794520994225973, 2.697186533604757, -0.9027928870967408, 1.1570861339569092, 3.123086452484131],
    "gripper_vertical": [1.418738842010498, -1.2759456199458619, 1.2870314756976526, 1.557830734843872, 1.5609979629516602, 2.964608669281006],
    "gripper_down": [1.412574291229248, -1.2245715421489258, 1.5707538763629358, 1.2227379518696289, 1.5618265867233276, 2.960045576095581],
    "just_above_stirrer": [1.4119385480880737, -1.232708917265274, 1.5361388365374964, 1.2655228811451416, 1.5617036819458008, 2.9591991901397705],
    "in_front_of_white_bg": [0.9755352735519409, -1.2298626464656373, 1.5326388517962855, 1.2679366308399658, 1.5615804195404053, 2.5227737426757812],
    "above_home_holder": [1.7151169776916504, -0.9303394120982666, 0.9488051573382776, 1.4103073316761474, 1.499406337738037, 3.27805757522583],
    "readjustment": [1.7267637252807617, -0.8310088676265259, 0.8723586241351526, 1.5185677248188476, 1.5266249179840088, 3.2738213539123535],
    "return_to_holder": [1.7270193099975586, -0.7678989332965394, 1.0835111776935022, 1.2442163664051513, 1.527403473854065, 3.275404453277588]
    }

# Constants for movement
MOVEMENT_PARAMS = {
    "speed": 0.25,
    "acceleration": 0.5,
    "blending": 0.02,
}

def degreestorad(angles_deg):
    """Convert a list of angles from degrees to radians."""
    return [angle * (math.pi / 180) for angle in angles_deg]

def move_robot(robot, position):
    """Move robot to a specific joint position."""
    robot.move_joint_list(position, MOVEMENT_PARAMS["speed"], MOVEMENT_PARAMS["acceleration"], MOVEMENT_PARAMS["blending"])

def operate_gripper(gripper, position):
    """Operate the gripper: 0 for open, 140 for picking up, 255 for fully closed."""
    gripper.move(position, 125, 125)

def main():
    robot = URControl(ip="192.168.0.2", port=30003)
    gripper = RobotiqGripper()
    gripper.connect("192.168.0.2", 63352)

    # Open gripper initially
    operate_gripper(gripper, 0)  # Open the gripper
    
    # Perform robot movements and gripper actions
    move_robot(robot, ROBOT_POSITIONS["home"])
    print("Moved to home position")

    time.sleep(1)
    
    # Sample handling process
    operate_gripper(gripper, 0)  # Open gripper
    move_robot(robot, ROBOT_POSITIONS["sample_vial"])
    print("Moved to sample vial position")

    operate_gripper(gripper, 140)  # Close the gripper to pick up the sample (gripper at 140)

    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["up_vertical"])
    print("Moved to up vertical position")

    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["above_stirrer"])
    print("Moved to above stirrer position")

    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["in_stirrer"])
    operate_gripper(gripper, 0)  # Open gripper to release the sample
    print("Moved to in stirrer position")

    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["above_stirrer"])
    print("Moved back above stirrer")

    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["gripper_vertical"])
    print("Moved gripper vertically")

    time.sleep(30)  # Stirring process (30 seconds) update this please when it comes to it

    move_robot(robot, ROBOT_POSITIONS["gripper_down"])
    operate_gripper(gripper, 140)  # Close the gripper to pick up sample
    print("Moved to gripper down position")

    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["just_above_stirrer"])
    print("Moved just above stirrer")
    
    time.sleep(1)
    move_robot(robot, ROBOT_POSITIONS["in_front_of_white_bg"])
    print("Moved to white background")

    # Initialize webcam
    cam = cv2.VideoCapture(0)

    # Create a window to display the feed
    cv2.namedWindow("test")

    # Thresholds
    blue_pixel_threshold = 100  # Minimum blue pixels required to consider it "blue"
    reaction_threshold = 500  # Total required blue pixels for successful detection
    blue_pixel_below_threshold_duration = 5  # Number of seconds below threshold before stopping

    # Track blue pixel count over time
    blue_pixel_counts = []
    times = []

    # Define Region of Interest (ROI)
    roi_x, roi_y, roi_w, roi_h = 200, 150, 260, 280  

    # CSV file path
    csv_file_path = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/blue_pixel_data.csv")

    # Track time
    start_time = time.time()
    last_logged_time = -1
    below_threshold_counter = 0  # Track how long the reaction is not blue

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

            # Only log data once per second
            if elapsed_seconds > last_logged_time:
                last_logged_time = elapsed_seconds  # Update last log time
                blue_pixel_counts.append((elapsed_seconds, blue_pixel_count))
                print(f"Time: {elapsed_seconds}s, Blue Pixels: {blue_pixel_count}")

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

            # Draw ROI on frame
            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
            cv2.imshow("test", frame)

            # Convert mask to displayable format
            blue_mask_display = cv2.merge([blue_mask.astype(np.uint8) * 255] * 3)
            cv2.imshow("Blue Mask", blue_mask_display)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Release webcam
        cam.release()
        cv2.destroyAllWindows()

        # Save CSV file
        try:
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Time (Seconds)", "Blue Pixel Count"])
                writer.writerows(blue_pixel_counts)
            print(f"Data successfully saved in: {csv_file_path}")
        except Exception as e:
            print(f"Error while saving CSV file: {e}")

# Define file paths
csv_file_path = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/blue_pixel_data.csv")
rate_constant_file = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/rate_constant.txt")
graph_file = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/kinetic_analysis_plot.png")

def read_and_process_csv(file_path):
    """Reads CSV file containing time and blue pixel count data."""
    try:
        data = pd.read_csv(file_path)

        # Extract time and intensity (blue pixel count)
        time_values = data.iloc[:, 0].values
        intensity_values = data.iloc[:, 1].values

        # Ensure valid values exist
        if len(time_values) < 2 or len(intensity_values) < 2:
            print("Error: Not enough data points in the CSV file.")
            return None, None

        # Remove NaN, Inf, or negative values
        valid_indices = ~np.isnan(intensity_values) & ~np.isinf(intensity_values) & (intensity_values >= 0)
        time_values = time_values[valid_indices]
        intensity_values = intensity_values[valid_indices]

        if len(time_values) < 2:
            print("Error: Insufficient valid data points after filtering.")
            return None, None

        # Stop analysis if all intensity values are zero
        if np.all(intensity_values == 0):
            print("No blue pixels detected. No reaction occurred. Skipping analysis.")
            return None, None

        # Normalize intensity values
        max_intensity = max(intensity_values)
        concentration_values = intensity_values / max_intensity if max_intensity > 0 else intensity_values

        return time_values, concentration_values

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None, None

# Kinetic Models
def zero_order_model(t, k, C0):
    """Zero-order reaction model: C = C0 - k*t"""
    return C0 - k * t

def first_order_model(t, k, C0):
    """First-order reaction model: C = C0 * exp(-k*t)"""
    return C0 * np.exp(-k * t)

def second_order_model(t, k, C0):
    """Second-order reaction model: 1/C = 1/C0 + k*t"""
    return 1 / (1/C0 + k * t)

def fit_kinetics(time_values, concentration_values):
    """Fits experimental data to zero-order, first-order, and second-order models and determines the best fit."""

    if len(time_values) < 2 or len(concentration_values) < 2:
        print("Error: Not enough data points for curve fitting.")
        return None, None

    # Remove NaN, Inf, and Zero values
    valid_indices = ~np.isnan(concentration_values) & ~np.isinf(concentration_values) & (concentration_values > 0)
    time_values = time_values[valid_indices]
    concentration_values = concentration_values[valid_indices]

    if len(time_values) < 2:
        print("Error: Insufficient valid data points after filtering.")
        return None, None

    C0 = concentration_values[0]

    try:
        # Fit Zero-Order Model
        popt_zero, _ = curve_fit(zero_order_model, time_values, concentration_values, p0=[0.01, C0])

        # Fit First-Order Model
        popt_first, _ = curve_fit(first_order_model, time_values, concentration_values, p0=[0.01, C0])

        # Fit Second-Order Model (Check for Zero Concentrations Before Taking Reciprocal)
        if np.all(concentration_values > 0):
            popt_second, _ = curve_fit(second_order_model, time_values, 1/concentration_values, p0=[0.01, C0])
            k_second, _ = popt_second
        else:
            print("Skipping Second-Order Fit: Concentration contains zero values.")
            k_second = None

        # Extract rate constants
        k_zero, _ = popt_zero
        k_first, _ = popt_first

        # Determine best-fit model
        best_model, best_k, best_fit_func = None, None, None
        best_r_squared = -np.inf  # To track best fit

        models = [
            ("Zero-Order", k_zero, zero_order_model),
            ("First-Order", k_first, first_order_model),
            ("Second-Order", k_second, second_order_model) if k_second is not None else None
        ]

        for model in models:
            if model:
                model_name, k_value, fit_func = model
                residuals = concentration_values - fit_func(time_values, k_value, C0)
                ss_tot = np.sum((concentration_values - np.mean(concentration_values)) ** 2)
                r_squared = 1 - (np.sum(residuals ** 2) / ss_tot)

                if r_squared > best_r_squared:
                    best_r_squared = r_squared
                    best_model = model_name
                    best_k = k_value
                    best_fit_func = fit_func

        # Print results
        print(f"Best Fit Model: {best_model}")
        print(f"Rate Constant (k): {best_k:.5f}")

        # Save rate constant to a text file
        with open(rate_constant_file, "w") as file:
            file.write(f"Best Fit Model: {best_model}\n")
            file.write(f"Rate Constant (k): {best_k:.5f}\n")

        print(f"Rate constant saved to: {rate_constant_file}")

        # Plot and save graph
        plt.figure(figsize=(8,6))
        plt.scatter(time_values, concentration_values, label="Experimental Data", color="blue")
        plt.plot(time_values, best_fit_func(time_values, best_k, C0), 'r-', label=f"Best Fit ({best_model})")

        plt.xlabel("Time (s)")
        plt.ylabel("Normalized Concentration")
        plt.title(f"Kinetic Analysis - {best_model} Model")
        plt.legend()
        plt.grid()

        plt.savefig(graph_file)
        print(f"Graph saved to: {graph_file}")

        plt.show()

        return best_k, best_model

    except Exception as e:
        print(f"Error in curve fitting: {e}")
        return None, None

def analyze_kinetics(file_path):
    """Reads data from CSV and determines reaction rate constant."""
    time_values, concentration_values = read_and_process_csv(file_path)

    # Stop if no valid data is found
    if time_values is None or concentration_values is None:
        print("Skipping kinetic analysis due to insufficient data.")
        return

    return fit_kinetics(time_values, concentration_values)

# Run analysis after reaction data is saved
analyze_kinetics(csv_file_path)

#Finish Off Robot Movement

time.sleep(2)
move_robot(robot, ROBOT_POSITIONS["above_home_holder"])
print("Moved above home holder")

time.sleep(1)
move_robot(robot, ROBOT_POSITIONS["readjustment"])
print("readjustment")
    
time.sleep(1)
move_robot(robot, ROBOT_POSITIONS["return_to_holder"])
print("Moved to return holder position")

# Open the gripper after completion
operate_gripper(gripper, 0)  # Open the gripper to finish

if __name__ == "__main__":
    main()
