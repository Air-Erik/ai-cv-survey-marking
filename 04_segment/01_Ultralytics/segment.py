import os
from ultralytics import YOLO
from PIL import Image

# Load a model
model = YOLO('C:\\Repos\\Ayrapetov\\07_AI_project\\04_segment\\01_Ultralytics\\runs\\segment\\train23\\weights\\best.pt')  # load a pretrained model

# Путь к папке с изображениями
pth_raw = 'C:\\Repos\\Ayrapetov\\07_AI_project\\02_mark\\images'
source = []
for dirpath, dirnames, filenames in os.walk(pth_raw):
    for filename in filenames:
        source.append(os.path.join(dirpath, filename))

# Запуск модели
results = model(source, stream=True, agnostic_nms=True, overlap_mask=False)  # generator of Results objects

for r in results:
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    image_name = r.path.split("\\")[-1:][0]
    im.save(f'result/{image_name}')
