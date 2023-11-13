import os, sys, argparse

from util import save_dict, load_dict, add_suffix_to_filename, join_pairs_images, delete_dict
from detect_lsh import find_near_duplicates

def get_pairs_sameimage(results_dict, threshold):
  similar_imgs = []

  # Iterate through the nested dictionaries
  for foldername in results_dict.keys():
    fullpath = results_dict[foldername]['path']
    for img1_name in results_dict[foldername]['results'].keys():
      for img2_name in results_dict[foldername]['results'][img1_name].keys():
        value = results_dict[foldername]['results'][img1_name][img2_name]

        if value >= threshold:
          full_path_img1 = os.path.join(fullpath, img1_name)
          full_path_img2 = os.path.join(fullpath, img2_name)
          similar_imgs.append([full_path_img1, full_path_img2, value])
                 
  return similar_imgs


def main(argv):
    parser = argparse.ArgumentParser(description="Efficient detection of near-duplicate images using locality sensitive hashing")
    parser.add_argument("-i", "--input_filename", type=str, default="", required=True, help="path of the input file with the imags paths")
    parser.add_argument("-o", "--output_filename", type=str, default="", required=True, help="name of the file for the results with lsh")
    parser.add_argument("-s", "--hash_size", type=int, default=16, help="hash size for the signatures")
    parser.add_argument("-t", "--threshold", type=float, default=0.75, help="threshold to decide which images are similar")
    parser.add_argument("-a", "--aux_file", type=str, default=None, help="auxiliar file to save continuosly the outputs obtained")

    args = parser.parse_args()
    IMGS_PATH_DICT_NAME = args.input_filename
    RESULTS_DICT_NAME = args.output_filename
    PAIRS_DICT_NAME = add_suffix_to_filename(RESULTS_DICT_NAME, 'pairs')
    JOINED_DICT_NAME = add_suffix_to_filename(PAIRS_DICT_NAME, 'joined')
    AUX_DICT_NAME = args.aux_file
    HASHSIZE = args.hash_size
    THRESHOLD = args.threshold

    images_dict = load_dict(IMGS_PATH_DICT_NAME)

    redo = True
    if load_dict(JOINED_DICT_NAME) is not None:
      confirmation = input(f"Do you wish to recalculate the lsh? (y/n): ").lower()
      if confirmation == 'y':
        print('Recalculating')
      elif confirmation == 'n':
        print('Will Continue Skipping LSH again.')
        redo = False
      else:
        print('Invalid Input.')
        sys.exit()

    if redo:
      metric_dict = None
      if AUX_DICT_NAME is not None:
        metric_dict = load_dict(AUX_DICT_NAME) # returns None if doesnt find it
      
      if metric_dict is None:
        metric_dict = {}

      total_comparisons = 0
      for folder_name in images_dict.keys():
        print('folder:', folder_name)
        if folder_name not in metric_dict.keys():
          pathdir = images_dict[folder_name]['path']
          pathdir_res = images_dict[folder_name]['path_resized']

          threshold = 0.0
          near_duplicates = find_near_duplicates(pathdir_res, threshold, HASHSIZE, HASHSIZE)
          if near_duplicates:
            # print(f"Found {len(near_duplicates)} near-duplicate images in {pathdir_res} (threshold {threshold:.2%})")
            metric_dict[folder_name] = {'results':{}, 'path':pathdir, 'path_resize': pathdir_res}
            for a,b,s in near_duplicates:
              a = os.path.basename(a)
              b = os.path.basename(b)
              if a not in metric_dict[folder_name]['results'].keys():
                metric_dict[folder_name]['results'][a] = {}
              metric_dict[folder_name]['results'][a][b] = s
            total_comparisons += len(near_duplicates)
          
          save_dict(metric_dict, AUX_DICT_NAME)
        else:
          print('skipped, already done')
      
      print('total comparisons:', total_comparisons)
      save_dict(metric_dict, RESULTS_DICT_NAME)

      images_similar = get_pairs_sameimage(metric_dict, THRESHOLD)
      save_dict(images_similar, PAIRS_DICT_NAME)

      joined_images = join_pairs_images(images_similar)
      save_dict(joined_images, JOINED_DICT_NAME)

      delete_dict(AUX_DICT_NAME)
      print('Done')



if __name__ == "__main__":
    main(sys.argv)