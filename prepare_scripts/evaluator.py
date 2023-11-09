import os

def get_sameimage(results_dict, method='mse'):
  similar_imgs = []

  # Iterate through the nested dictionaries
  for foldername in results_dict.keys():
    fullpath = results_dict[foldername]['path']
    for img1_name in results_dict[foldername]['results'].keys():
      for img2_name in results_dict[foldername]['results'][img1_name].keys():
        value = results_dict[foldername]['results'][img1_name][img2_name]

        if method == 'histogram':
          if value >= 0.75:
            full_path_img1 = os.path.join(fullpath, img1_name)
            full_path_img2 = os.path.join(fullpath, img2_name)
            similar_imgs.append([full_path_img1, full_path_img2, value])
                 
  return similar_imgs
