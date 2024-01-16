import yaml
import psycopg
from psycopg import sql


# Скрипт прочитывает метки и названия классов из файлов datasets
# И заполняет таблицу classes в базе данных postgreSQL

# Путь к yaml файлу датасета
pth_dataset = 'C:/Repos/Ayrapetov/07_AI_project/01_learn/datasets/AutoCAD_Topo_v7/data.yaml'

# Извлекает из датасета имена для классов
with open(pth_dataset) as yaml_file:
    yaml_read_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
# Извлекает из словаря только имена классов
class_names = yaml_read_data['names']
class_count = yaml_read_data['nc']

print(class_names)

query = sql.SQL('''
    INSERT INTO {table_val} (class) VALUES ({len_val});
''').format(
    table_val=sql.Identifier('workflow', 'classes'),
    len_val=sql.SQL('), (').join(sql.Placeholder() * len(class_names))
)


with psycopg.connect('dbname=ai_project user=ayrapetov_es \
password=1111') as conn:
    conn.execute(
        query, class_names
    )
