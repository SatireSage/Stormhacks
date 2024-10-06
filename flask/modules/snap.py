import datetime
import os
import time

import cv2


def list_webcams():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        ret, frame = cap.read()
        if ret:
            arr.append(index)
        cap.release()
        index += 1
    return arr


def capture_images_from_webcam(cam_index):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"Cannot open webcam {cam_index}")
        return

    # Ensure the directory exists
    image_dir = "../static/images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print("Press Enter to take a photo, or 'q' then Enter to quit.")
    while True:
        user_input = input()
        if user_input.lower() == "q":
            break
        else:
            print("Taking photo in 5 seconds...")
            time.sleep(5)
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                continue
            else:
                # Generate unique filename using timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(image_dir, f"captured_image_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Image saved as {filename}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # List all available webcams
    webcams = list_webcams()

    if not webcams:
        print("No webcams found.")
    else:
        # If only one webcam is found, use it directly
        if len(webcams) == 1:
            cam_index = webcams[0]
            print(f"Using webcam at index {cam_index}")
            capture_images_from_webcam(cam_index)
        else:
            print("Available webcams:")
            for i, cam in enumerate(webcams):
                print(f"{i}: Webcam {cam}")

            # Ask user to select a webcam
            selected = int(input("Select the webcam index to capture images: "))

            if selected < 0 or selected >= len(webcams):
                print("Invalid selection")
            else:
                # Capture images from the selected webcam
                cam_index = webcams[selected]
                capture_images_from_webcam(cam_index)
