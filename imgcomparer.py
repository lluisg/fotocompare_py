import os, cv2
import numpy as np
from tqdm import tqdm

from skimage.metrics import structural_similarity as ssim


def mse_approach(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar"
    return err


def histogram_approach(imageA, imageB):
    # Compute histograms
    hist_img1 = cv2.calcHist([imageA], [0], None, [256], [0, 256])
    hist_img2 = cv2.calcHist([imageB], [0], None, [256], [0, 256])

    # Normalize histograms
    hist_img1 /= hist_img1.sum()
    hist_img2 /= hist_img2.sum()

    # Calculate histogram intersection
    hist_intersection = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_INTERSECT)
    return hist_intersection


def compare_2images(img1, img2, method, printing):
  # Read images
  img1 = cv2.imread(img1)
  img2 = cv2.imread(img2)

  # Convert images to grayscale
  gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

  # Compute metric result
  if method == 'mse':
    value = mse_approach(gray_img1, gray_img2)
  elif method == 'ssim':
    value = ssim(gray_img1, gray_img2, full=False)
  elif method == 'histogram':
    value = histogram_approach(gray_img1, gray_img2)

  if printing:
    # Concatenate images side by side
    combined_img = np.hstack((gray_img1, gray_img2))

    # Display the combined image
    cv2.imshow(str(value), combined_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  return value

def compare_all(pathfolder, imgs_arr, method, printing):
  # gets the values comparing all with all
  result_dict = {}
  total_comp = 0

  n = len(imgs_arr)
  for i in tqdm(range(n)):
    element1 = imgs_arr[i]
    full_e1 = os.path.join(pathfolder, element1)
    result_dict[element1] = {}
    for j in range(i + 1, n):
      element2 = imgs_arr[j]
      full_e2 = os.path.join(pathfolder, element2)

      metric = compare_2images(full_e1, full_e2, method, printing)
      result_dict[element1][element2] = metric
      total_comp += 1

  return result_dict, total_comp


def compare_improved(pathfolder, imgs_arr, method, printing):
  # gets the values using a somewhat improved version of a comparer
  result_dict = {}
  n = len(imgs_arr)
  for i in tqdm(range(n)):
    element1 = imgs_arr[i]
    full_e1 = os.path.join(pathfolder, element1)
    result_dict[element1] = {}
    for j in range(i + 1, n):
      element2 = imgs_arr[j]
      full_e2 = os.path.join(pathfolder, element2)

      metric = compare_2images(full_e1, full_e2, method, printing)
      result_dict[element1][element2] = metric

  return result_dict


def compare_list_images(pathfolder, pathfolder_resized, imgs_arr, method='mse', printing=True, improved=False):
  metric_dict = {'results':{}, 'path':pathfolder, 'path_resized': pathfolder_resized}

  if not improved: # the way of comparing will be simpler
    metric_dict['results'], num_comp = compare_all(pathfolder_resized, imgs_arr, method, printing)
  else:
    metric_dict['results'], num_comp = compare_improved(pathfolder_resized, imgs_arr, method, printing)
  print('num_comp:', num_comp)

    
  return metric_dict, num_comp
