import sys
import psycopg
import pandas as pd
import numpy as np
from ultralytics import YOLO
from psycopg import sql

sys.path.insert(0, '../03_init_database')

from image_creator import file_names_and_pth_creator

# Получение списков полных путей и имен изображений
full_path_images, image_names = file_names_and_pth_creator()

# Название схемы и таблиц и папки с обученными весами
schema_name_in_db = 'workflow'
class_table_name_in_db = 'classes'
image_table_name_in_db = 'image_data'
mark_table_name_in_db = 'raw_mark_data'
custom_weights = 'weight'

# Создание SQL запроса на добавление данных о рамках
query_input = sql.SQL('''
    INSERT INTO {table_raw_mark}
    (x_1, y_1, x_2, y_2, percent, image_name, class_id, image_id, plan_id)
    SELECT
        %s, %s, %s, %s, %s, %s,
        (SELECT class_id FROM {table_class} WHERE class = %s),
        (SELECT image_id FROM {table_image} WHERE image_name = %s),
        (SELECT plan_id FROM {table_image} WHERE image_name = %s)
''').format(
    table_raw_mark=sql.Identifier(schema_name_in_db, mark_table_name_in_db),
    table_class=sql.Identifier(schema_name_in_db, class_table_name_in_db),
    table_image=sql.Identifier(schema_name_in_db, image_table_name_in_db)
)

query_unique = sql.SQL('''
    SELECT DISTINCT
        x_1,
        y_1,
        x_2,
        y_2,
        image_name
    FROM {table_raw_mark}
''')

# Загрузка модели для пердсказания
model = YOLO(f"{custom_weights}/best.pt")

# Предсказание. Параметр conf определяет достоверный порог вероятности при
# котором засчитывается обнаружение
results = model(full_path_images, conf=0.70)

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
    df['class_name'] = class_names[class_id]
    df['image_name'] = image_name
    # Приведение к типу float64 потому что postgreSQL ругается на тип
    # данных float32
    df = df.astype({'x1': 'float64',
                    'y1': 'float64',
                    'x2': 'float64',
                    'y2': 'float64',
                    'percent': 'float64'})

    # Подключение к базе данных и исполнение SQL запроса на вставку данных
    with psycopg.connect('dbname=ai_project user=API_write_data \
    password=1111') as conn:
        # Вывод запросов перед выполнением
        print('SQL-запрос на вставку записей в БД:')
        print(query_input.as_string(conn))

        for i in df.index:
            conn.execute(
                query_input, (
                    df['x1'][i],
                    df['y1'][i],
                    df['x2'][i],
                    df['y2'][i],
                    df['percent'][i],
                    df['image_name'][i],
                    df['class_name'][i],
                    df['image_name'][i],
                    df['image_name'][i]
                )
            )
