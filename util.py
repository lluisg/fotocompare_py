import os, json

def save_dict(my_dict, my_file, results=True):
  # saves the dictionary in a json file
  # if results is true it will save it inside the results folder
  if results:
    if not os.path.exists('results'):
      os.makedirs('results')
    my_file = os.path.join('results', my_file)

  with open(my_file, 'w') as json_file:
    json.dump(my_dict, json_file, indent=4)


def load_dict(my_file, results=True):
  # loads a json file if it exists, if it doesnt returns None
  try:
    if results:
      my_file = os.path.join('results', my_file)

    with open(my_file, 'r') as file:
      metric_dict = json.load(file)
  except:
    metric_dict = None

  return metric_dict


def delete_dict(my_file, results=True):
  # removes a file if it exists
  if results:
    my_file = os.path.join('results', my_file)
  
  if os.path.exists(my_file):
    os.remove(my_file)


def add_suffix_to_filename(filename, suffix):
  # adds the suffix specified to the filename
  base, ext = os.path.splitext(filename)
  new_filename = f"{base}_{suffix}{ext}"
  return new_filename


def join_pairs_images(imgs_array):
  # from a list of pairs, it joins all the elements pairs that contains a shared element
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


def replace_dict_elements_with_indices(main_list, sublist):
  # given a dictionary of lists, it replaces the elements on the lists, by the index given the main list
  for key, sub_array in sublist.items():
      for i in range(len(sub_array)):
          if sub_array[i] in main_list:
              index = main_list.index(sub_array[i])
              sub_array[i] = index
    