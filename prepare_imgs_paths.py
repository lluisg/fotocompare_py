import os, sys, argparse
from tqdm import tqdm

from util import save_dict

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
      extension = img_name.split('.')[-1].lower()
      if extension in image_extensions:
        images_paths[folder_name]['images'].append(img_name)

  return images_paths


def main(argv):
    # Argument parser
    parser = argparse.ArgumentParser(description="Get the path for all the images in the folder and subfolders indicated")
    parser.add_argument("-i", "--input_path", type=str, default="", required=True, help="path of the input folder")
    parser.add_argument("-o", "--output_filename", type=str, default="paths_images.json", help="name of the file where output results will go")
    
    args = parser.parse_args()
    FOLDER_PATH = args.input_path
    IMGS_PATH_DICT_NAME = args.output_filename

    paths_dict = get_subfolders_files(FOLDER_PATH)
    images_dict = clean_images(paths_dict)

    save_dict(images_dict, IMGS_PATH_DICT_NAME)
    print('Done')


if __name__ == "__main__":
    main(sys.argv)