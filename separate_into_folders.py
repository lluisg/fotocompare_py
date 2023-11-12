import os, argparse, shutil, sys
from tqdm import tqdm

from util import save_dict, load_dict, add_suffix_to_filename


def move_imgs(photo_paths):
  ind = 0
  for photo_list in tqdm(photo_paths):
    folder_name = f"similar_imgs_{ind + 1}"

    photo_folder = os.path.dirname(photo_list[0])
    destination_folder = os.path.join(photo_folder, folder_name)
    if not os.path.exists(destination_folder):
      os.makedirs(destination_folder)

    for photo_path in photo_list:
      photo_name = os.path.basename(photo_path)
      destination_path = os.path.join(destination_folder, photo_name)

      shutil.move(photo_path, destination_path)
    ind += 1


def main(argv):
    parser = argparse.ArgumentParser(description="Efficient detection of near-duplicate images using locality sensitive hashing")
    parser.add_argument("-i", "--input_filename", type=str, default="", required=True, help="path of the input file with the results")

    args = parser.parse_args()
    RESULTS_DICT_NAME = args.input_filename
    JOINED_DICT_NAME = add_suffix_to_filename(add_suffix_to_filename(RESULTS_DICT_NAME, 'pairs'), 'joined')

    joined_images = load_dict(JOINED_DICT_NAME)
    move_imgs(joined_images)
    print('Done')


if __name__ == "__main__":
    main(sys.argv)