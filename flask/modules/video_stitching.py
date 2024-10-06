import os

import cv2


def check_video(video_name: str) -> bool:
    """
    Checks if the video name already exists. If it does, append a number to prevent overwriting the existing video.

    Parameters:
        video_name (str):

    Returns:
        bool: 

    """


def check_image_folder(image_folder: str) -> bool:
    """
    Check if the image folder exits and if there are images present.

    """

    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]

    if not images:
        return False


# def stitch(params**) -> None:
def stitch(image_folder: str, video_name: str, fps: int, seconds_per_image: int, height: int, width: int, isColor: bool) -> None:
    """
    Combines static images into a video.

    Parameters:
        image_folder (str)
        video_name (str):
        ...

    Returns:
        bool: 

    """

    # Call check image folder
        # If folder and images exist then get the images
    # Call check video name

    first_image_path = os.path.join(image_folder, images[0])
    image_details = cv2.imread(first_image_path)

    if image_details is None:
        return

    height, width, layers = image_details.shape

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
