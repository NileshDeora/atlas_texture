from flask import Flask, request, jsonify, send_file
from PIL import Image
from moviepy.editor import VideoFileClip, ImageClip, clips_array, ColorClip
import os
import tempfile

app = Flask(__name__)

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
    
    # Load videos and resize them
    videos = [VideoFileClip(path).resize(newsize=(cell_width, cell_height)) for path in video_paths]

    # Determine the maximum duration for the videos
    max_duration = max([video.duration for video in videos]) if videos else 10  # Default to 10 seconds if no videos

    # Load images and convert them to static video clips
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
    output_video_path = "output_media_grid_final.mp4"
    video_grid.write_videofile(output_video_path, codec='libx264')
    return output_video_path
# Define your image and video paths

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

@app.route('/create-grid', methods=['POST'])
def create_grid():
    if 'images' not in request.files:
        return jsonify({"error": "No images part in the request"}), 400
    if 'videos' not in request.files:
        return jsonify({"error": "No videos part in the request"}), 400

    image_paths = request.files.getlist('images')
    video_paths = request.files.getlist('videos')

    # Grid configuration
    grid_rows = 3
    grid_cols = 3
    target_width = 1920
    target_height = 1080

    if len(video_paths) == 0:
        print("create image texture")
        output_path = create_image_grid(image_paths, grid_rows, grid_cols, target_width, target_height)
        print("Output saved at:", output_path)

    else:
        # Create the media grid and get the output path
        print("create video texture")
        output_path = create_video_grid(image_paths, video_paths, grid_rows, grid_cols, target_width, target_height)
        print("Output saved at:", output_path)

    return send_file(output_path, as_attachment=True, attachment_filename='output_media_grid_final.mp4')

if __name__ == '__main__':
    app.run(debug=True, port=5000)