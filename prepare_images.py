import json, os

from prepare_scripts.image_paths import get_subfolders_files, clean_images
from prepare_scripts.fotocomparer import compare_list_images
from prepare_scripts.evaluator import get_sameimage

def save_dict(my_dict, my_file):
  if not os.path.exists('results'):
    os.makedirs('results')

  with open(os.path.join('results', my_file), 'w') as json_file:
    json.dump(my_dict, json_file, indent=4)


if __name__ == "__main__":
  RECALCULATE = True

  folder_path = "C:\\Users\\Lluis\\Desktop\\Projects\\fotocompare_py\\fotos"
  folder_path = "C:\\Users\\Lluis\\Desktop\\Projects\\fotocompare_py\\small_fotos"
  # folder_path = "C:\\Users\\Lluis\\Pictures"
  paths_dict = get_subfolders_files(folder_path)
  images_dict = clean_images(paths_dict)

  save_dict(images_dict, 'paths_images.json')

  # methods = ['mse', 'ssim', 'histogram']
  methods = ['histogram']
  for method in methods:
    jsonname_values = 'images_'+method+'_values.json'
    jsonfolder_values = os.path.join('results', jsonname_values)
    jsonname_results = 'images_'+method+'_results.json'
    jsonfolder_results = os.path.join('results', jsonname_results)

    if os.path.exists(jsonfolder_values) and not RECALCULATE:
      with open(jsonfolder_values, 'r') as file:
        metric_dict = json.load(file)
        print(f"File {jsonfolder_values} exists. Content loaded.")
    else:
      metric_dict = {}
      for folder_name in images_dict.keys():
        print('folder:', folder_name)
        metric_dict[folder_name] = compare_list_images(images_dict[folder_name]['path'], 
                                                      images_dict[folder_name]['images'], 
                                                      method,
                                                      False)
      
      save_dict(metric_dict, jsonname_values)

    images_similar = get_sameimage(metric_dict, method)
    save_dict(images_similar, jsonname_results)


  with open('data_prepared', 'w') as file:
    pass
  print('Done')


      

       

