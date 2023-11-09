import cv2
import numpy as np
from tqdm import tqdm
import os

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


def resize_image(image, target_size=(600, 600)):
    return cv2.resize(image, target_size)


def compare_2images(img1, img2, method, printing):
  # Read images
  img1 = cv2.imread(img1)
  img2 = cv2.imread(img2)

  # Resize images to a common size
  img1 = resize_image(img1)
  img2 = resize_image(img2)

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

def compare_list_images(pathfolder, imgs_arr, method='mse', printing=True):
  metric_dict = {'results':{}, 'path':pathfolder}

  n = len(imgs_arr)

  for i in tqdm(range(n)):
    element1 = imgs_arr[i]
    full_e1 = os.path.join(pathfolder, element1)
    metric_dict['results'][element1] = {}
    for j in range(i + 1, n):
      element2 = imgs_arr[j]
      full_e2 = os.path.join(pathfolder, element2)

      metric = compare_2images(full_e1, full_e2, method, printing)
      metric_dict['results'][element1][element2] = metric
    
  return metric_dict
