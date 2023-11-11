import os, json

def save_dict(my_dict, my_file, results=True):
  if results:
    if not os.path.exists('results'):
      os.makedirs('results')
    my_file = os.path.join('results', my_file)

  with open(my_file, 'w') as json_file:
    json.dump(my_dict, json_file, indent=4)


def load_dict(my_file, results=True):
  try:
    if results:
      my_file = os.path.join('results', my_file)

    with open(my_file, 'r') as file:
      metric_dict = json.load(file)
  except:
    metric_dict = None

  return metric_dict

def add_suffix_to_filename(filename, suffix):
  base, ext = os.path.splitext(filename)
  new_filename = f"{base}_{suffix}{ext}"
  return new_filename
