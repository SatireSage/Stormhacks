import logging
import os

import cv2

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum log level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
)


def sort_images(image_folder: str) -> list:
    images = list(os.listdir(image_folder))
    return sorted(images)


def check_video(video_name: str) -> str:
    """
    Checks if the video name already exists. If it does, appends a
    number to prevent overwriting the existing video.

    Parameters:
        video_name (str): The desired name of the video file.

    Returns:
        str: A valid video filename (new or adjusted).
    """
    base_name, ext = os.path.splitext(video_name)
    counter = 1

    while os.path.exists(video_name):
        video_name = f"{base_name}_{counter}{ext}"
        counter += 1

    return video_name


def check_image_folder(image_folder: str) -> bool:
    """
    Check if the image folder exists and if there are images present.

    Parameters:
        image_folder (str): Path to the folder containing images.

    Returns:
        bool: True if the folder contains valid images, False otherwise.
    """
    if not os.path.exists(image_folder):
        return False

    images = [
        img
        for img in os.listdir(image_folder)
        if img.endswith((".png", ".jpg", ".jpeg"))
    ]

    return bool(images)


def stitch(
    image_folder: str, video_name: str, fps: int, seconds_per_image: int, **kwargs
) -> None:
    """
    Combines static images into a video.

    Parameters:
        image_folder (str): The folder containing images.
        video_name (str): Desired output video name.
        fps (int): Frames per second.
        seconds_per_image (int): How long each image should appear in the video.
        **kwargs: Additional optional parameters for height, width, and isColor.
                 - height (int): Desired height of the video frames. If not provided, it will be based on the first image.
                 - width (int): Desired width of the video frames. If not provided, it will be based on the first image.
                 - isColor (bool): Whether the video should be in color or grayscale. Defaults to True.
    """
    # Optional parameters with defaults
    height = kwargs.get("height", None)
    width = kwargs.get("width", None)
    isColor = kwargs.get("isColor", True)

    # Check if the image folder exists and contains images
    if not check_image_folder(image_folder):
        logging.info("No valid images found in the folder.")
        return

    # Get list of images in the folder
    images = sort_images(image_folder=image_folder)

    # Check if the video name is already taken and get a valid filename
    video_name = check_video(video_name)

    # Load the first image to determine frame size if height and width are not provided
    first_image_path = os.path.join(image_folder, images[0])
    image_details = cv2.imread(first_image_path)

    if image_details is None:
        logging.info("Error reading the first image.")
        return

    # Set height and width based on the first image if not provided
    if height is None or width is None:
        height, width, layers = image_details.shape

    # Initialize the video writer
    video = cv2.VideoWriter(
        filename=video_name,
        fourcc=cv2.VideoWriter_fourcc(*"avc1"),
        fps=fps,
        frameSize=(width, height),
        isColor=isColor,
    )

    # Write each image to the video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)

        if frame is None:
            logging.info(f"Error reading image {image_path}, skipping.")
            continue

        # Resize frame if necessary
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))

        # Write the image multiple times based on fps and seconds_per_image
        # for _ in range(fps * seconds_per_image):
        video.write(frame)

    video.release()
    logging.info(f"Video saved as {video_name}")
