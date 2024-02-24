# Let's visualize our images

# view_image_phil("/content/drive/MyDrive/data","phil_pred.jpg")
# !wget https://github.com/filipposkar/phil/blob/main/maria.jpg?raw=true -O maria.jpg
# view_image_phil("/content", "maria.jpg")

'''
this function shows a =n image stored in a folder
input:
  target_dir:   the target folder
  target_image: the target image (the image to show)
'''

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

def view_image_phil(target_dir, target_image):

  # Read in the image and plot it using matplotlib
  img = mpimg.imread(target_dir + "/" + target_image)
  plt.imshow(img)
  #plt.axis("off")

  return True
