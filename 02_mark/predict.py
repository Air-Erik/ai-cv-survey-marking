import sys
import psycopg
import pandas as pd
import numpy as np
from ultralytics import YOLO
from psycopg import sql

sys.path.insert(0, '../03_init_database')

from image_creator import file_names_and_pth_creator

# Исполнение кода
source, file_names = file_names_and_pth_creator()

# Название схемы и таблиц
schema_name_in_db = 'workflow'
mark_table_name_in_db = 'raw_mark_data'

# Название папки с обученными весами
custom_weights = 'weight'

# Загрузка модели для пердсказания
model = YOLO(f"{custom_weights}/best.pt")

# Предсказание. Параметр conf определяет достоверный порог вероятности при
# котором засчитывается обнаружение
results = model(source, conf=0.70)

# Обработка результатов анализа
for r in results:

    # Запись результатов работы нейросети. 
    # Рамки, проценты, имена обработанных изображений и номера классов
    frames = r.boxes.xyxy.cpu().numpy()
    percent = r.boxes.conf.cpu().numpy()
    image_name = r.path.split('\\')[-1:][0]
    class_id = r.boxes.cls.cpu().numpy()
    class_id = int(class_id[0])

    # Создание списка имен классов и перевод их к виду словаря
    # в виде {номер: название класса}
    class_names = r.names
    class_names = {key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in class_names.items()}

    # Создание таблицы pandas
    df = pd.DataFrame(frames, columns=['x1', 'y1', 'x2', 'y2'])
    df['percent'] = pd.DataFrame(percent)
    df['class_names'] = class_names[class_id]
    df['image_name'] = image_name
    # Приведение к типу float64 потому что postgreSQL ругается на тип
    # данных float32
    df = df.astype({'x1': 'float64',
                    'y1': 'float64',
                    'x2': 'float64',
                    'y2': 'float64',
                    'percent': 'float64'})
    print(df)
