import cv2
import numpy as np

# Initialize webcam
cam = cv2.VideoCapture(0)

# Create a window to display the feed
cv2.namedWindow("test")

img_counter = 0

# Threshold for the number of blue pixels required (100 in this case)
blue_pixel_threshold = 100  # Adjust this as needed

while True:
    # Capture frame from webcam
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Range for blue color in HSV space
    # You can adjust these values to better match the shade of blue
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])

    # Captures areas in the frame that are blue
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Count the number of blue pixels
    blue_pixel_count = np.count_nonzero(mask)

    # Check if the number of blue pixels exceeds the threshold
    if blue_pixel_count > blue_pixel_threshold:
        print("The reaction has been successful")

    # Show the original frame and the mask (to visualize the blue detection)
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

# Release resources and close the windows
cam.release()
cv2.destroyAllWindows()
