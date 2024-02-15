from ultralytics import YOLO
from PIL import Image

# Load a model
model = YOLO('yolov8n-seg.pt')  # load a pretrained model

# Define path to directory containing images and videos for inference
source = '../../02_mark/images/План 1_0_0.jpg'

# Run inference on the source
results = model('test.jpg', stream=True)  # generator of Results objects

for r in results:
    im_array = r.plot(boxes=False)
    im = Image.fromarray(im_array[..., ::-1])
    image_name = r.path.split("\\")[-1:][0]
    im.save(f'result/{image_name}')
    print(r.masks)
