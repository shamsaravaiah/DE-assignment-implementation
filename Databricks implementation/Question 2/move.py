
import os
import random
import shutil

def move_images(source_dir, destination_dir, percentage):
    # Get list of image files in the source directory
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Calculate the number of images to move
    num_images_to_move = int(len(image_files) * percentage)

    # Randomly select images to move
    images_to_move = random.sample(image_files, num_images_to_move)

    # Move selected images to the destination directory
    for image in images_to_move:
        source_path = os.path.join(source_dir, image)
        destination_path = os.path.join(destination_dir, image)
        shutil.move(source_path, destination_path)

    print(f"Successfully moved {num_images_to_move} images to {destination_dir}")

# Example usage:
source_directory = "/Users/sham_sara/Downloads/cell_images/Uninfected\ Train"
destination_directory = "/Users/sham_sara/Downloads/cell_images/Uninfected\ Test/images"
percentage_to_move = 0.2  # 20%

move_images(source_directory, destination_directory, percentage_to_move)






