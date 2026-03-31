"""
... is the place where you need to fill in
"""

import cv2
from google.colab.patches import cv2_imshow
import numpy as np

def image_sharpening(image, c=-1.0):
    ###########################################################
    """Return a sharpened version of the image, using cv2.Laplacian.
    # First, call GaussianBlur to blur the image 
    # Second, call Laplacian function on blurred_image to obtain the edge_map
    # Third, obtain the sharpened image by adding edge_map to original image 
    """
    blurred_image = cv2.GaussianBlur(image, (3,3), 0) 
    edge_map = ... # Hint: you can refer to https://docs.opencv.org/3.4/d5/db5/tutorial_laplace_operator.html, default parameter: cv2.CV_16S, (3,3) 
    cv2_imshow(abs(edge_map))
    image = image.astype(float)
    edge_map = edge_map.astype(float)
    g_sharp = ... # Hint: you can refer to the slide Topic 3: Spatial Filtering Page 128
    ###########################################################
    g_sharp = np.maximum(g_sharp, np.zeros(g_sharp.shape))
    g_sharp = np.minimum(g_sharp, 255 * np.ones(g_sharp.shape))
    g_sharp = g_sharp.round().astype(np.uint8)
    return g_sharp


if __name__ == "__main__":

    image = cv2.imread("test3.jpg", 0)
    cv2_imshow(image)
    ###########################################################
    """Please call this function with different values of Magnifying factor and analyze the results."""
    c = -1.0  # c is the Magnifying factor for image and edge map in the slide Topic 3: Spatial Filtering Page 128
    result = image_sharpening(image, c=c)
    ###########################################################
    cv2_imshow(result)
