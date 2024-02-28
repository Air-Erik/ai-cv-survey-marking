from skimage.morphology import skeletonize, thin
from skimage import io
import matplotlib.pyplot as plt
from skimage.util import invert
from skimage.color import rgb2gray

image = io.imread("2.jpg")

# Если ваше изображение цветное, преобразуйте его в оттенки серого
image_gray = rgb2gray(image)

# Invert the horse image
image_inverted = invert(image_gray)

# perform skeletonization
skeleton = skeletonize(image_inverted)
thinned = thin(image_inverted)
thinned_partial = thin(image_inverted, max_num_iter=25)


# display results
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12),
                         sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

ax[2].imshow(thinned, cmap=plt.cm.gray)
ax[2].axis('off')
ax[2].set_title('thinned', fontsize=20)

ax[3].imshow(thinned_partial, cmap=plt.cm.gray)
ax[3].axis('off')
ax[3].set_title('thinned_partial', fontsize=20)

fig.tight_layout()
plt.show()
