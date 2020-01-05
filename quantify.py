import sys
# from scipy.misc import imread
import scipy.misc
import imageio
from scipy.linalg import norm
# import numpy.linalg
from scipy import sum, average
import cv2
import numpy as np 


gnm = []
gn0 = []

def ret_quant():
    global gnm
    global gn0
    x = np.mean(gnm)
    y = np.mean(gn0) 
    z = np.max(gnm)
    z1 = np.max(gn0)
    gnm = []
    gn0 = []
    # return x, y
    return x, y, z, z1

def quant(file1, file2):
    # cv2.imshow('file1', file1)
    # cv2.imshow('file2', file2)
    cv2.waitKey(27)
    # file1, file2 = sys.argv[1:1+2]
    # read images as 2D arrays (convert to grayscale for simplicity)
    # img1 = to_grayscale(imageio.imread(file1).astype(float))
    # cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img1 = cv2.cvtColor(file1, cv2.COLOR_BGR2GRAY)
    # img2 = to_grayscale(imageio.imread(file2).astype(float))
    img2 = cv2.cvtColor(file2, cv2.COLOR_BGR2GRAY)
    # print(img1)
    # print(img2)
    # compare
    n_m, n_0 = compare_images(img1, img2)
    # print ("Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size)
    # print ("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size)
    # f = open('quant.txt','a')
    # f.write(format(n_m))
    # f.write(',\t')
    # f.write(format(n_0))
    # f.close()
    
    global gnm
    global gn0
    gnm.append(n_m/img1.size)
    gn0.append(n_0/img1.size)
    
def compare_images(img1, img2):
    # normalize to compensate for exposure difference
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)
def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr
def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng
# if __name__ == "__main__":
#     main()
