import cv2
import numpy as np

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


def compare_2images(gray_img1, gray_img2, method):
  # Compute metric result
  if method == 'mse':
    value = mse_approach(gray_img1, gray_img2)
  elif method == 'ssim':
    value = ssim(gray_img1, gray_img2, full=False)
  elif method == 'histogram':
    value = histogram_approach(gray_img1, gray_img2)
  return value
