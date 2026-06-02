import cv2
import os


def extract_keyframes(
    video_path,
    output_dir,
    num_frames=8
):
    """
    Extract evenly spaced frames from a video.

    Returns:
        list[str]: Paths to extracted images
    """

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    if total_frames == 0:
        cap.release()
        return []

    frame_paths = []

    step = max(
        total_frames // num_frames,
        1
    )

    for i in range(num_frames):

        frame_no = i * step

        cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_no
        )

        success, frame = cap.read()

        if not success:
            continue

        frame_path = os.path.join(
            output_dir,
            f"frame_{i}.jpg"
        )

        cv2.imwrite(
            frame_path,
            frame
        )

        frame_paths.append(frame_path)

    cap.release()

    return frame_paths