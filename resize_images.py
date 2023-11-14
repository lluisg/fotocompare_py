import os, cv2, shutil, sys, argparse
from tqdm import tqdm

from util import save_dict, load_dict

def resize_image(image, target_size=(500, 500)):
    return cv2.resize(image, target_size)


def main(argv):
    parser = argparse.ArgumentParser(description="Efficient detection of near-duplicate images using locality sensitive hashing")
    parser.add_argument("-i", "--input_folder", type=str, default="", required=True, help="path of the input folder where the images")
    parser.add_argument("-d", "--input_dictionary", type=str, default="", required=True, help="path of the input file with the imags paths")
    parser.add_argument("-o", "--output_folder", type=str, default="", required=True, help="name of the folder where the resized images will go")
    parser.add_argument("-r", "--resize", type=int, default=800, help="size for the resized images NxN")

    args = parser.parse_args()
    IMGS_FOLDER = args.input_folder
    IMGS_PATH_DICT_NAME = args.input_dictionary
    IMGS_RESIZED_FOLDER = args.output_folder
    SIZE = args.resize

    RESIZE_SIZE = (SIZE, SIZE)

    redo = True
    if os.path.exists(IMGS_RESIZED_FOLDER):
      confirmation = input(f"Do you wish to restart the destination folder? (y/n): ").lower()
      if confirmation == 'y':
        shutil.rmtree(IMGS_RESIZED_FOLDER)
        print('Folder Deleted')
      elif confirmation == 'n':
        print('Will Process Without Deleting.')
        redo = False
      else:
        print('Invalid Input.')
        sys.exit()

    images_dict = load_dict(IMGS_PATH_DICT_NAME)

    for folder in images_dict.keys():
      print('folder:', folder)
      folderpath = images_dict[folder]['path']

      new_folderpath = folderpath.replace(IMGS_FOLDER, IMGS_RESIZED_FOLDER)
      if not os.path.exists(new_folderpath):
        os.makedirs(new_folderpath)
      images_dict[folder]['path_resized'] = new_folderpath

      for imgname in tqdm(images_dict[folder]['images']):
        img_path = os.path.join(folderpath, imgname)
        dest_img_path = os.path.join(new_folderpath, imgname)

        if redo: # only resize again the image if indicated
          original_img = cv2.imread(img_path)
          resized_img = resize_image(original_img, RESIZE_SIZE)

          cv2.imwrite(dest_img_path, resized_img)

      save_dict(images_dict, IMGS_PATH_DICT_NAME)
      print('Done')


if __name__ == "__main__":
    main(sys.argv)