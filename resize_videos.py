import cv2
import os

def resize_video(input_path, output_path, scale_factor=0.25):
    # Open the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_path}")
        return

    # Get original video dimensions
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))

    # Set new dimensions to 75% of original
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # Create a VideoWriter object to write the resized video
    out = cv2.VideoWriter(output_path, codec, fps, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame
        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Write the resized frame to the output video
        out.write(resized_frame)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Video has been resized and saved to {output_path}")

def process_videos(input_directory, output_directory, scale_factor=0.25):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".mp4"):  # You can add other video file extensions if needed
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            resize_video(input_path, output_path, scale_factor)

if __name__ == "__main__":
    input_directory = "./input"  # Replace with your input directory path
    output_directory = "./output"  # Replace with your output directory path

    process_videos(input_directory, output_directory, scale_factor=0.25)
