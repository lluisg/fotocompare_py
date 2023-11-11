import os
import subprocess
import shutil
from tqdm import tqdm
from itertools import combinations

from util import save_dict, load_dict


def join_images(imgs_array):
  print('joining')
  imgs_newarray = [[x1,x2] for x1,x2,_ in imgs_array]

  used_list = []
  joined_imgs = []

  for set_img in imgs_newarray:
    img1, img2 = set_img
    if img1 not in used_list and img2 not in used_list:
        # if none image is already used, they dont have any conecction and are added automatically
        joined_imgs.append(set_img)
        used_list.append(img1)
        used_list.append(img2)
    elif img1 in used_list and img2 in used_list:
      #  if both images are already used, they are already added
       pass
    elif img1 in used_list and img2 not in used_list:
      #  if only img1 has been used, we add img2 in the same set
      for set_joined in joined_imgs:
         if img1 in set_joined:
            set_joined.append(img2)
            used_list.append(img2)
            break
    elif img1 not in used_list and img2 in used_list:
      #  if only img2 has been used, we add img1 in the same set
      for set_joined in joined_imgs:
         if img2 in set_joined:
            set_joined.append(img1)
            used_list.append(img1)
            break
    else:
       print('problem---------------------------------------------------------------------')
       print(img1)
       print(img2)
       print(used_list)
       print(joined_imgs)
       break
  
  return joined_imgs


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


if __name__ == "__main__":
  REDO = True
  DESCRIPTOR_NAME = 'separated_into_folders'

  if not os.path.exists(DESCRIPTOR_NAME) or REDO:
    # METHODS = ['mse', 'ssim', 'histogram']
    METHODS = ['histogram']

    for method in METHODS:
      print('method:', method)
      results_filepath = 'images_'+method+'_results.json'
      results_filepath = 'fotos_'+method+'_results.json'
      joined_filepath = 'images_'+method+'_joined.json'
      joined_filepath = 'fotos_'+method+'_joined.json'

      results = load_dict(results_filepath)
      joined_images = join_images(results)
      save_dict(joined_images, joined_filepath)

      move_imgs(joined_images)

    with open(DESCRIPTOR_NAME, 'w') as file:
      pass
  print('Done')
