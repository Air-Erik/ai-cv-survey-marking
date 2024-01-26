import sys
import psycopg
from ultralytics import YOLO
from PIL import Image
from psycopg import sql

from image_creator import image_creator_func

image_creator_func()


'''
# Название папки с обученными весами
custom_weights = 'weight'

# Загрузка модели для пердсказания
model = YOLO(f"{custom_weights}/best.pt")

# Предсказание. Параметр conf определяет достоверный порог вероятности при
# котором засчитывается обнаружение
results = model(source, conf=0.70)
'''
