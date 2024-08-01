from PIL import Image
from moviepy.editor import VideoFileClip, ImageClip, clips_array, ColorClip
import os
import tempfile
# Helper function to create a blank video clip
def create_blank_clip(size, duration, color=(0, 0, 0)):
    return ColorClip(size=size, color=color).set_duration(duration)

# Function to create a static video clip from an image
def create_image_clip(image_path, duration, size):
    return ImageClip(image_path).set_duration(duration).resize(newsize=size)

# Function to create a video grid with images and videos
def create_video_grid(image_paths, video_paths, grid_rows, grid_cols, target_width, target_height):
    cell_width = target_width // grid_cols
    cell_height = target_height // grid_rows

    # Load and resize videos
    valid_videos = []
    for path in video_paths:
        try:
            video = VideoFileClip(path).resize(newsize=(cell_width, cell_height))
            valid_videos.append(video)
        except Exception as e:
            print(f"Skipping video {path} due to error: {e}")

    # Determine the maximum duration for the videos
    max_duration = max([video.duration for video in valid_videos]) if valid_videos else 10  # Default to 10 seconds if no videos

    # Loop videos to match the maximum duration
    videos = [video.loop(duration=max_duration) for video in valid_videos]

    # Convert image paths to static video clips
    image_clips = [create_image_clip(path, max_duration, (cell_width, cell_height)) for path in image_paths]

    # Combine images and videos
    media_clips = videos + image_clips

    # Ensure there are enough clips to fill the grid
    while len(media_clips) < grid_rows * grid_cols:
        media_clips.append(create_blank_clip((cell_width, cell_height), max_duration))

    # Create grid layout for the media clips
    grid_clips = []
    for i in range(grid_rows):
        row_clips = media_clips[i * grid_cols: (i + 1) * grid_cols]
        grid_clips.append(row_clips)

    # Concatenate the video rows to create the final grid
    video_grid = clips_array(grid_clips)

    # Save the grid video and return the path
    # output_video_path = os.path.join(tempfile.gettempdir(), "output_media_grid_final.mp4")
    output_video_path = "output_video.mp4"
    video_grid.write_videofile(output_video_path, codec='libx264', audio=False)
    return output_video_path

def create_image_grid(image_paths, grid_rows, grid_cols, target_width, target_height):
    print('done')
    images = [Image.open(path) for path in image_paths]
    # Resize images to fit the grid cells
    cell_width = target_width // grid_cols
    cell_height = target_height // grid_rows

    resized_images = [img.resize((cell_width, cell_height)) for img in images]

    # Create a new blank image for the grid
    grid_image = Image.new('RGB', (target_width, target_height))

    # Paste images into the grid
    for i, img in enumerate(resized_images):
        row = i // grid_cols
        col = i % grid_cols
        grid_image.paste(img, (col * cell_width, row * cell_height))
    # Save the resulting image
    output_path = "output_grid_image.png"
    grid_image.save(output_path)
    return output_path

image_paths = [
 
    # "./input/7.webp",
    # "./input/8.webp",
    # "./input/9.webp",
    # add more image paths
]
video_paths = [
    "./input/1.mp4",
    "./input/2.mp4",
    "./input/3.mp4",
    "./input/4.mp4",
    "./input/5.mp4",
    "./input/6.mp4",
    # "./input/7.mp4",
    # "./input/8.mp4",
    # "./input/9.mp4",
    # "./input/10.mp4",
    # "./input/11.mp4",
    # "./input/12.mp4",
    # "./input/13.mp4",
    # "./input/14.mp4",
    # "./input/15.mp4",
]

# Grid configuration
grid_rows = 3
grid_cols = 3
target_width = 960
target_height = 540

if len(video_paths) == 0:
    print("create image texture")
    output_path = create_image_grid(image_paths, grid_rows, grid_cols, target_width, target_height)
    print("Output saved at:", output_path)

else:
    # Create the media grid and get the output path
    print("create video texture")
    output_path = create_video_grid(image_paths, video_paths, grid_rows, grid_cols, target_width, target_height)
    print("Output saved at:", output_path)
