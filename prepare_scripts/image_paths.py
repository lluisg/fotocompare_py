import os
import glob

def get_subfolders_files(root_folder):
  subfolder_files = {}

  for folderpath, _, filenames in os.walk(root_folder):
    subfolder_files[folderpath] = filenames

  return subfolder_files

def clean_images(paths_dict, image_extensions=['jpg', 'jpeg', 'png']):
  images_paths = {}

  for path in paths_dict.keys():
    folder_name = os.path.basename(path)
    images_paths[folder_name] = {'images':[], 'path':path}
    for img_name in paths_dict[path]:
      extension = img_name.split('.')[-1]
      if extension in image_extensions:
        images_paths[folder_name]['images'].append(img_name)

  return images_paths
