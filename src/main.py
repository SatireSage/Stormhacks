from modules import video_stitching as vs


def main():
    """Main program

    Parameters:
        argument1 (none): No arguments

    Returns:
        int: Returning value

    """
    # Code goes over here.
    vs.stitch("/mnt/c/Stormhacks/src/modules/test-images")
    return 0


if __name__ == "__main__":
    main()
