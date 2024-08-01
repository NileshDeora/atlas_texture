from PIL import Image
from moviepy.editor import VideoFileClip, ImageClip, clips_array, ColorClip



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
    output_path = "output_logo_image.png"
    grid_image.save(output_path)
    return output_path




image_paths = [
 
    "./input/1.webp",
    "./input/2.webp",
    "./input/3.webp",
    "./input/4.webp",
    "./input/5.webp",
    "./input/6.webp",
    "./input/7.webp",
    "./input/8.webp",
    "./input/9.webp",

    # add more image paths
]
# Grid configuration
grid_rows = 3
grid_cols = 3
target_width = 1080
target_height = 1080

output_path = create_image_grid(image_paths, grid_rows, grid_cols, target_width, target_height)
print("Output saved at:", output_path)