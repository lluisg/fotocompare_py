import os
from PIL import Image
from tqdm import tqdm

def get_image_sizes(folder_path):
    image_sizes = []

    # Traverse through the folder and subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files):
            # Check if the file is an image (you can add more extensions if needed)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Get the full file path
                file_path = os.path.join(root, file)

                # Open the image using Pillow
                with Image.open(file_path) as img:
                    # Get the size of the image
                    size = img.size

                    # Append the size to the list
                    image_sizes.append((file_path, size))

    return image_sizes

# Specify the folder path
folder_path = "C:\\Users\\Lluis\\Desktop\\Projects\\fotocompare_py\\fotos"
# folder_path = "C:\\Users\\Lluis\\Pictures"

# Get the image sizes
sizes_list = get_image_sizes(folder_path)

small_width = 9999
small_height = 9999
for size in sizes_list:
    width, height = size[-1]

    if width < small_width:
        small_width = width
    if height < small_height:
        small_height = height


# Print the image sizes
for file_path, size in sizes_list:
    print(f"Image: {file_path}, Size: {size}")

print('smaller:', small_width, small_height)
