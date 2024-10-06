import os

import cv2


def stitch(image_folder):
    video_name = "Stitched-Video.mp4"

    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]

    if not images:

        return

    first_image_path = os.path.join(image_folder, images[0])
    image_details = cv2.imread(first_image_path)

    if image_details is None:

        return

    height, width, layers = image_details.shape
    fps = 1
    seconds_per_image = 1

    video = cv2.VideoWriter(
        filename=video_name,
        fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
        fps=fps,
        frameSize=(width, height),
        isColor=True,
    )

    # Write each image to the video
    for image in images:

        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)

        for _ in range(fps * seconds_per_image):
            video.write(frame)

    video.release()
