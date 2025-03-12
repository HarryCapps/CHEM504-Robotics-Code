import cv2
import numpy as np
import time
import csv
import os

# Initialize webcam
cam = cv2.VideoCapture(0)

# Create a window to display the feed
cv2.namedWindow("test")

# Thresholds
blue_pixel_threshold = 100  # Minimum number of blue pixels to detect reaction
reaction_threshold = 500  # Total required blue pixels over time
blue_pixel_below_threshold_duration = 5  # Time for "reaction is no longer blue"
time_limit = 60  # Run for 60 seconds

# Track blue pixel count over time
blue_pixel_counts = []
times = []

# Define Region of Interest (ROI)
roi_x, roi_y, roi_w, roi_h = 200, 150, 260, 280  

# CSV file path
csv_file_path = os.path.expanduser("~/Code/chem504-2425_GroupA/examples/blue_pixel_data.csv")

# Track time
start_time = time.time()
last_logged_time = -1  # Ensures first log at t=0

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

            # Print progress for debugging
            print(f"Time: {elapsed_seconds}s, Blue Pixels: {blue_pixel_count}")

        # Draw ROI on frame
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)
        cv2.imshow("test", frame)

        # Convert mask to displayable format
        blue_mask_display = cv2.merge([blue_mask.astype(np.uint8) * 255] * 3)
        cv2.imshow("Blue Mask", blue_mask_display)

        # Stop after 60 seconds
        if elapsed_seconds >= time_limit:
            break

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

    # Check if enough blue was detected
    if sum(count for _, count in blue_pixel_counts) >= reaction_threshold:
        print("Sample vial is blue")
    else:
        print("Sample vial did not reach the blue threshold")
