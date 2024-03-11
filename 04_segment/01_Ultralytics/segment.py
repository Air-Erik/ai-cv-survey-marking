import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from ultralytics import YOLO
from PIL import Image

# Load a model
model = YOLO('C:\\Repos\\Ayrapetov\\07_AI_project\\04_segment\\01_Ultralytics\\runs\\segment\\train12\\weights\\best.pt')  # load a pretrained model

# Define path to directory containing images and videos for inference
source = '../../02_mark/images/План 1_1_1.jpg'

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects

for r in results:
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    image_name = r.path.split("\\")[-1:][0]
    im.save(f'result/{image_name}')
    class_id = r.boxes.cls.cpu().numpy()
    pol = (r[1].masks.xy)
    box = (r.boxes.xyxy.cpu().numpy())

x = []
new_pol = LineString(pol[0])
for i in pol[0]:
    x.append((i[0], i[1]))


print(np.asarray(new_pol.coords))
