import cv2
import numpy as np
import time
import csv

# Initialize webcam
cam = cv2.VideoCapture(0)

# Create a window to display the feed
cv2.namedWindow("test")

img_counter = 0

# Thresholds
blue_pixel_threshold = 100  # Number of blue pixels to trigger detection
reaction_threshold = 500  # Threshold for "Sample vial is blue"
blue_pixel_below_threshold_duration = 5  # Number of consecutive seconds below threshold to print "reaction is no longer blue"
time_limit = 60  # Time limit for 60 seconds

# To track the time and blue pixels
blue_pixel_counts = []
times = []

# Keep track of the blue reaction duration
below_threshold_counter = 0
reaction_started = False
reaction_ended = False

# Define Region of Interest (ROI) for detection (x, y, width, height)
roi_x, roi_y, roi_w, roi_h = 200, 150, 400, 300  # Adjust these values based on your camera setup

# Open a CSV file to save the results
with open('blue_pixel_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time (Seconds)", "Blue Pixel Count"])

    start_time = time.time()

    while True:
        # Capture frame from webcam
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Crop the frame to the ROI
        roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Convert the frame to RGB (no conversion needed as we are already working with RGB)
        # Check blue channel: For blue detection, blue channel should be high and red/green low
        blue_channel = roi_frame[:, :, 0]  # Blue channel (OpenCV uses BGR by default)
        green_channel = roi_frame[:, :, 1]  # Green channel
        red_channel = roi_frame[:, :, 2]  # Red channel

        # Define thresholds for blue detection (you can fine-tune these values)
        blue_mask = (blue_channel > 150) & (green_channel < 100) & (red_channel < 100)

        # Count the number of blue pixels in the ROI
        blue_pixel_count = np.count_nonzero(blue_mask)
        
        # Track time
        elapsed_time = time.time() - start_time
        elapsed_seconds = int(elapsed_time)
        
        # If the blue pixel count is above the threshold, we consider it "blue"
        if blue_pixel_count >= blue_pixel_threshold:
            below_threshold_counter = 0  # Reset the counter if blue pixels are detected
            if not reaction_started:
                print("Sample vial is blue")
                reaction_started = True
        else:
            # If blue pixel count is below the threshold, we count how many seconds it stays low
            below_threshold_counter += 1
            if below_threshold_counter >= blue_pixel_below_threshold_duration and not reaction_ended:
                print("The reaction is no longer blue")
                reaction_ended = True

        # Append the data for this second
        blue_pixel_counts.append(blue_pixel_count)
        times.append(elapsed_seconds)

        # Write the data to the CSV file
        writer.writerow([elapsed_seconds, blue_pixel_count])

        # Display the original frame, ROI frame, and the mask (to visualize the blue detection)
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (0, 255, 0), 2)  # Draw ROI rectangle
        cv2.imshow("test", frame)
        cv2.imshow("Blue Mask", blue_mask.astype(np.uint8) * 255)  # Display the blue pixel mask (converted to 255 for visibility)

        # Stop the loop after 60 seconds
        if elapsed_seconds >= time_limit:
            break

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

    # After 60 seconds, stop the webcam and close the windows
    cam.release()
    cv2.destroyAllWindows()

    # Check if enough blue was present throughout the 60 seconds
    if sum(blue_pixel_counts) >= reaction_threshold:
        print("Sample vial is blue")
    else:
        print("Sample vial did not reach the blue threshold")
