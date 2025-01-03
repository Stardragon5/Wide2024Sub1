
# Python program for Detection of a specific color using OpenCV with Python
import cv2
import rospy
from std_msgs.msg import Int32
import numpy as np
import time

if __name__ == '__main__':
    # Initialize node with a valid name (no spaces)
    rospy.init_node("color_detection")

    # Color Publisher
    color_pub = rospy.Publisher('camera_color', Int32, queue_size=10)

    # Get parameter values
    frequency = rospy.get_param('~/frequency', 2)

    # Webcamera no 0 is used to capture the frames
    cap = cv2.VideoCapture(0)

    # Set variables
    rate = rospy.Rate(frequency)
    color = 0

    # Data Collection Loop
    while not rospy.is_shutdown():
        # Captures the live stream frame-by-frame
        ret, frame = cap.read()
        if not ret:
            rospy.logwarn("Failed to capture frame.")
            continue

        # Create new frame
        size = frame.shape
        frame1 = np.zeros((int(size[0]/10), int(size[1]/10), size[2]), dtype=np.uint8)
        size1 = frame1.shape

        # Pulls every tenth pixel
        for i in range(0, int(size[0]/10)):
            for j in range(0, int(size[1]/10)):
                frame1[i, j] = frame[10 * i, 10 * j]

        # Color BGR Definitions
        lower_red = np.array([9, 13, 112])
        upper_red = np.array([41, 35, 171])
        lower_orange = np.array([7, 40, 136])
        upper_orange = np.array([49, 104, 193])
        lower_yellow = np.array([10, 100, 134])
        upper_yellow = np.array([46, 152, 186])
        lower_green = np.array([95, 100, 29])
        upper_green = np.array([160, 181, 109])
        lower_blue = np.array([90, 40, 10])
        upper_blue = np.array([160, 110, 52])
        lower_purple = np.array([80, 30, 40])
        upper_purple = np.array([152, 84, 128])
        lower_black = np.array([24, 19, 17])
        upper_black = np.array([70, 70, 60])

        # Color masks & Summation
        dem = 255 * size1[0] * size1[1]
        thresh = 0.2
        while True:
            # Initialize color as 0 (none)
            color = 0

            # Define masks and check each color
            red_mask = cv2.inRange(frame1, lower_red, upper_red)
            red_t = np.sum(np.sum(red_mask)) / dem
            rospy.loginfo('Red: %f', red_t)
            if red_t > thresh:
                color = 1  # Red
                rospy.loginfo("Detected color: Red")
                break

            orange_mask = cv2.inRange(frame1, lower_orange, upper_orange)
            orange_t = np.sum(np.sum(orange_mask)) / dem
            rospy.loginfo('Orange: %f', orange_t)
            if orange_t > thresh:
                color = 2  # Orange
                rospy.loginfo("Detected color: Orange")
                break

            yellow_mask = cv2.inRange(frame1, lower_yellow, upper_yellow)
            yellow_t = np.sum(np.sum(yellow_mask)) / dem
            rospy.loginfo('Yellow: %f', yellow_t)
            if yellow_t > thresh:
                color = 3  # Yellow
                rospy.loginfo("Detected color: Yellow")
                break

            green_mask = cv2.inRange(frame1, lower_green, upper_green)
            green_t = np.sum(np.sum(green_mask)) / dem
            rospy.loginfo('Green: %f', green_t)
            if green_t > thresh:
                color = 4  # Green
                rospy.loginfo("Detected color: Green")
                break

            blue_mask = cv2.inRange(frame1, lower_blue, upper_blue)
            blue_t = np.sum(np.sum(blue_mask)) / dem
            rospy.loginfo('Blue: %f', blue_t)
            if blue_t > thresh:
                color = 5  # Blue
                rospy.loginfo("Detected color: Blue")
                break

            purple_mask = cv2.inRange(frame1, lower_purple, upper_purple)
            purple_t = np.sum(np.sum(purple_mask)) / dem
            rospy.loginfo('Purple: %f', purple_t)
            if purple_t > thresh:
                color = 6  # Purple
                rospy.loginfo("Detected color: Purple")
                break

            black_mask = cv2.inRange(frame1, lower_black, upper_black)
            black_t = np.sum(np.sum(black_mask)) / dem
            rospy.loginfo('Black: %f', black_t)
            if black_t > 1.5 * thresh:
                color = 7  # Black
                rospy.loginfo("Detected color: Black")
                break

            rospy.loginfo("No color detected")
            break

        # Publish detected color
        color_pub.publish(color)

        # Display the frame with rotation and pause if necessary
        frame1 = cv2.rotate(frame1, cv2.ROTATE_180)
        # Uncomment the following line if you want to display the frame:
        # cv2.imshow('frame1', frame1)

        # Comment out the above line if you don't want to display the frame
        # in a headless environment (e.g., SSH session without display)

        # Control the flow based on the key pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        # Sleep at the defined rate
        rate.sleep()

    # Release the camera and close windows
    cv2.destroyAllWindows()
    cap.release()

