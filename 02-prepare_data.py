import os, sys

from util import save_dict, load_dict
from imgcomparer import compare_list_images
from detect import find_near_duplicates

def get_sameimage(results_dict, method='mse'):
  THRESHOLD_HISTOGRAM = 0.75

  similar_imgs = []

  # Iterate through the nested dictionaries
  for foldername in results_dict.keys():
    fullpath = results_dict[foldername]['path']
    for img1_name in results_dict[foldername]['results'].keys():
      for img2_name in results_dict[foldername]['results'][img1_name].keys():
        value = results_dict[foldername]['results'][img1_name][img2_name]

        if method == 'histogram':
          if value >= THRESHOLD_HISTOGRAM:
            full_path_img1 = os.path.join(fullpath, img1_name)
            full_path_img2 = os.path.join(fullpath, img2_name)
            similar_imgs.append([full_path_img1, full_path_img2, value])
                 
  return similar_imgs


if __name__ == "__main__":
  REDO = True
  DESCRIPTOR_NAME = 'data_prepared'
  PRINT_IMAGES = False
  IMPROVED_COMPARATOR = False
  # with no improved_comparator it does total 456.022 comparisons (429 in smaller folder)
  # with improved_comparator it does total    1.522 comparisons (35 in smaller folder)

  if not os.path.exists(DESCRIPTOR_NAME) or REDO:
    IMGS_DICT_NAME = 'paths_images.json'
    # IMGS_DICT_NAME = 'paths_images_fotos.json'

    # METHODS = ['mse', 'ssim', 'histogram', 'lsh']
    METHODS = ['lsh']

    images_dict = load_dict(IMGS_DICT_NAME)

    for method in METHODS:
      jsonname_values = 'images_'+method+'_values.json'
      # jsonname_values = 'fotos_'+method+'_values.json'
      jsonname_results = 'images_'+method+'_results.json'
      # jsonname_results = 'fotos_'+method+'_results.json'

      metric_dict = load_dict(jsonname_values)
      if metric_dict is not None and not REDO:
        print(f"File {jsonname_values} exists. Content loaded.")
      else:
        metric_dict = {}
        total_comparisons = 0
        for folder_name in images_dict.keys():
          print('folder:', folder_name)

          if method == 'lsh':
            pathdir = images_dict[folder_name]['path_resized']
            pathdir_res = images_dict[folder_name]['path_resized']

            threshold = 0.0
            near_duplicates = find_near_duplicates(pathdir_res, threshold, 16, 16)
            if near_duplicates:
              print(f"Found {len(near_duplicates)} near-duplicate images in {pathdir_res} (threshold {threshold:.2%})")
              metric_dict[folder_name] = {'results':{}, 'path':pathdir}
              for a,b,s in near_duplicates:
                a = os.path.basename(a)
                b = os.path.basename(b)
                if a not in metric_dict[folder_name]['results'].keys():
                  metric_dict[folder_name]['results'][a] = {}
                metric_dict[folder_name]['results'][a][b] = s
              total_comparisons += len(near_duplicates)

          else:
            metric_dict[folder_name], num_comp = compare_list_images(images_dict[folder_name]['path'],
                                                                images_dict[folder_name]['path_resized'], 
                                                                images_dict[folder_name]['images'], 
                                                                method, PRINT_IMAGES, IMPROVED_COMPARATOR)
            total_comparisons += num_comp
        
        print('total comparisons:', total_comparisons)
        save_dict(metric_dict, jsonname_values)

      images_similar = get_sameimage(metric_dict, method)
      save_dict(images_similar, jsonname_results)

    with open(DESCRIPTOR_NAME, 'w') as file:
      pass
  print('Done')
