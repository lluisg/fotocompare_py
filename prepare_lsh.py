import os, sys, argparse

from util import save_dict, load_dict, add_suffix_to_filename
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

    args = parser.parse_args()
    IMGS_PATH_DICT_NAME = args.input_filename
    RESULTS_DICT_NAME = args.output_filename
    PAIR_DICT_NAME = add_suffix_to_filename(RESULTS_DICT_NAME, 'pairs')
    HASHSIZE = args.hash_size
    THRESHOLD = args.threshold

    images_dict = load_dict(IMGS_PATH_DICT_NAME)

    metric_dict = {}
    total_comparisons = 0
    for folder_name in images_dict.keys():
      print('folder:', folder_name)
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
    
    print('total comparisons:', total_comparisons)
    save_dict(metric_dict, RESULTS_DICT_NAME)

    images_similar = get_pairs_sameimage(metric_dict, THRESHOLD)
    save_dict(images_similar, PAIR_DICT_NAME)
    print('Done')


if __name__ == "__main__":
    main(sys.argv)