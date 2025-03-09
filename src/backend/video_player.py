import cv2

def pause():
    """Pauses the video and waits for keypress to resume or quit."""
    print("Paused. Press 'p' to resume, 'q' to quit.")
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord('p'):
            print("Resuming...")
            return False  # Resume
        elif key == ord('q'):
            print("Exiting...")
            return True  # Quit

def read_video(frames):
    """Displays video with frame navigation."""
    frame_idx = 0
    while True:
        cv2.imshow("Pose Skeleton", cv2.resize(frames[frame_idx], (0, 0), fx=0.25, fy=0.25))
        key = cv2.waitKey(0) & 0xFF

        if key == ord('d'):  # Next frame
            frame_idx = min(frame_idx + 1, len(frames) - 1)
        elif key == ord('a'):  # Previous frame
            frame_idx = max(frame_idx - 1, 0)
        elif key == ord('p'):  # Pause
            if pause():
                break
        elif key == ord('q'):  # Quit
            break

    cv2.destroyAllWindows()