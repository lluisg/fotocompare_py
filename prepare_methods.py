import os, sys, argparse, cv2
from tqdm import tqdm

from util import save_dict, load_dict, add_suffix_to_filename, join_pairs_images, replace_dict_elements_with_indices, delete_dict
from imgcomparer import compare_2images

def get_pairs_sameimage(results_dict, method, threshold, with_lsh):
  similar_imgs = []

  # Iterate through the nested dictionaries
  for foldername in results_dict.keys():
    fullpath = results_dict[foldername]['path']
    for img1_name in results_dict[foldername]['results'].keys():
      for img2_name in results_dict[foldername]['results'][img1_name].keys():
        value = results_dict[foldername]['results'][img1_name][img2_name]

        if value=='name' or (with_lsh and value == 'lsh') or (method in ['histogram'] and value >= threshold) or (method in ['mse'] and value < threshold):
          full_path_img1 = os.path.join(fullpath, img1_name)
          full_path_img2 = os.path.join(fullpath, img2_name)
          similar_imgs.append([full_path_img1, full_path_img2, value])
                 
  return similar_imgs


def compare_all(pathfolder, pathfolder_res, imgs_arr, method):
  # gets the values comparing all with all
  imgs_arr_fullpath = [os.path.join(pathfolder, x) for x in imgs_arr]
  imgs_arr_fullpath_res = [os.path.join(pathfolder_res, x) for x in imgs_arr]

  print('loading all images (and their gray version):')
  all_images = []
  all_gray_images = []
  for imgpath in tqdm(imgs_arr_fullpath_res):
    img = cv2.imread(imgpath)
    all_images.append(img)
    all_gray_images.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

  result_dict = {}
  total_comp = 0

  n = len(imgs_arr)
  for i in tqdm(range(n)):
    element1 = imgs_arr[i]
    gray_img1 = all_gray_images[i]

    result_dict[element1] = {}
    for j in range(i + 1, n):
      element2 = imgs_arr[j]
      gray_img2 = all_gray_images[j]

      if clean_name(element1) == clean_name(element2):
        metric = 'name'
      else:
        metric = compare_2images(gray_img1, gray_img2, method)
      result_dict[element1][element2] = metric
      total_comp += 1

  return result_dict, total_comp


def create_association_dict(arr_of_arr):
  new_dict = {}
  for arr in arr_of_arr:
    for el in arr:
      new_dict[el] = []
      for el2 in arr:
        if el != el2:
          new_dict[el].append(el2)
  return new_dict


def clean_name(name):
  name_no_ext = name.split('.')[0]
  name_lower = name_no_ext.lower()
  return name_lower


def compare_improved(pathfolder, pathfolder_res, imgs_arr, METHOD, lsh_file):
  # gets the values using a somewhat improved version of a comparer
  imgs_arr_fullpath = [os.path.join(pathfolder, x) for x in imgs_arr]
  imgs_arr_fullpath_res = [os.path.join(pathfolder_res, x) for x in imgs_arr]

  lsh_results = load_dict(lsh_file)

  lsh_association = create_association_dict(lsh_results)
  replace_dict_elements_with_indices(imgs_arr_fullpath, lsh_association)

  result_dict = {}
  total_comp = 0

  print('loading all images (and their gray version):')
  all_images = []
  all_gray_images = []
  for imgpath in tqdm(imgs_arr_fullpath_res):
    img = cv2.imread(imgpath)
    all_images.append(img)
    all_gray_images.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

  print('comparing images:')  
  n = len(imgs_arr)
  for i in tqdm(range(n)):
    element1 = imgs_arr[i]
    full_e1 = imgs_arr_fullpath[i]
    gray_img1 = all_gray_images[i]

    result_dict[element1] = {}

    # if the element has already been checked by the lsh, we will ignore all the ones that consider to be similar
    list_comparison = [x for x in range(i + 1, n)]
    if full_e1 in lsh_association.keys():
      for ind2ignore in lsh_association[full_e1]:
        if ind2ignore in list_comparison:
          element2 = imgs_arr[ind2ignore]
          result_dict[element1][element2] = 'lsh'
          list_comparison.remove(ind2ignore)

    for j in list_comparison:
      element2 = imgs_arr[j]
      gray_img2 = all_gray_images[j]

      if clean_name(element1) == clean_name(element2):
        metric = 'name'
      else:
        metric = compare_2images(gray_img1, gray_img2, METHOD)
      result_dict[element1][element2] = metric
      total_comp += 1

  return result_dict, total_comp


def main(argv):
    parser = argparse.ArgumentParser(description="Efficient detection of near-duplicate images using locality sensitive hashing")
    parser.add_argument("-i", "--input_filename", type=str, default="", required=True, help="path of the input file with the imags paths")
    parser.add_argument("-o", "--output_filename", type=str, default="", required=True, help="name of the file for the results with lsh")
    parser.add_argument("-l", "--lsh_filename", type=str, default=None, help="name of the file for the results with lsh")
    parser.add_argument("-t", "--threshold", type=float, default=0.75, help="threshold to decide which images are similar")
    parser.add_argument("-m", "--method", type=str, default="histogram", help="method to use for the comparison [histogram, mse, ssim]")
    parser.add_argument("-a", "--aux_file", type=str, default=None, help="auxiliar file to save continuosly the outputs obtained")

    args = parser.parse_args()
    IMGS_PATH_DICT_NAME = args.input_filename
    RESULTS_DICT_NAME = args.output_filename
    PAIRS_DICT_NAME = add_suffix_to_filename(RESULTS_DICT_NAME, 'pairs')
    JOINED_DICT_NAME = add_suffix_to_filename(PAIRS_DICT_NAME, 'joined')
    AUX_DICT_NAME = args.aux_file
    LSH_DICT_NAME = args.lsh_filename
    THRESHOLD = args.threshold
    METHOD = args.method

    IMPROVED_COMPARATOR = False
    JOINED_LSH_FILE = None
    if LSH_DICT_NAME is not None:
      IMPROVED_COMPARATOR = True
      JOINED_LSH_FILE = add_suffix_to_filename(add_suffix_to_filename(LSH_DICT_NAME, 'pairs'), 'joined')
      print('Will use improved comparator')
    else:
      print('Comaparator all vs all')

    images_dict = load_dict(IMGS_PATH_DICT_NAME)

    redo = True
    if load_dict(JOINED_DICT_NAME) is not None:
      confirmation = input(f"Do you wish to recalculate the "+str(METHOD)+"? (y/n): ").lower()
      if confirmation == 'y':
        print('Recalculating')
      elif confirmation == 'n':
        print('Will Continue Skipping '+METHOD+' again.')
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
        print('--')
        print('folder:', folder_name)
        if folder_name not in metric_dict.keys():
          pathfolder = images_dict[folder_name]['path']
          pathfolder_resized = images_dict[folder_name]['path_resized']
          list_images = images_dict[folder_name]['images']
          metric_dict[folder_name] = {'path':pathfolder, 'path_resized': pathfolder_resized}

          if not IMPROVED_COMPARATOR:
            metric_dict[folder_name]['results'], num_comp = compare_all(pathfolder, pathfolder_resized, list_images, METHOD)
          else:
            metric_dict[folder_name]['results'], num_comp = compare_improved(pathfolder, pathfolder_resized, list_images, METHOD, JOINED_LSH_FILE)
          total_comparisons += num_comp
        
          save_dict(metric_dict, AUX_DICT_NAME)
        else:
          print('skipped, already done')

      print('total comparisons:', total_comparisons)
      save_dict(metric_dict, RESULTS_DICT_NAME)

      images_similar = get_pairs_sameimage(metric_dict, METHOD, THRESHOLD, JOINED_LSH_FILE is not None)
      save_dict(images_similar, PAIRS_DICT_NAME)

      joined_images = join_pairs_images(images_similar)
      save_dict(joined_images, JOINED_DICT_NAME)

      delete_dict(AUX_DICT_NAME)
      print('Done')

if __name__ == "__main__":
    main(sys.argv)