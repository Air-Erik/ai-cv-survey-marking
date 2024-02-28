from skimage import io
import matplotlib.pyplot as plt
from skimage.filters import median

# Загрузка вашего изображения
image = io.imread("2.jpg")

# Применение медианного фильтра для уменьшения толщины линий
filtered_image = median(image)

# Отображение результатов
plt.imshow(filtered_image, cmap='gray')
plt.axis('off')
plt.show()
