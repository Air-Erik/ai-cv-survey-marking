import psycopg
from psycopg import sql


# Название схемы и таблиц
schema_name_in_db = 'workflow'
raw_mark_table_name_in_db = 'raw_mark_data'
mark_table_name_in_db = 'mark_data'

# SQL запрос на создание функции проверки строки на уникальность по  5 столбцам
query_befor_insert = sql.SQL('''
CREATE OR REPLACE FUNCTION before_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем наличие дубликатов перед вставкой
    IF EXISTS (
        SELECT 1
        FROM {table}
        WHERE x_1 = NEW.x_1
            AND y_1 = NEW.y_1
            AND x_2 = NEW.x_2
            AND y_2 = NEW.y_2
            AND image_name = NEW.image_name
    ) THEN
    -- Если дубликат найден, просто завершаем выполнение триггера
        RETURN NULL;
    END IF;

    -- Если проверка прошла успешно, возвращаем NEW для выполнения вставки
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
''').format(table=sql.Identifier(schema_name_in_db, raw_mark_table_name_in_db))

# SQL запрос на создание тригера перед вставкой для проверки уникальности
qurey_triger_before_insert = sql.SQL('''
CREATE TRIGGER check_unique_before_insert
BEFORE INSERT ON {table}
FOR EACH ROW
EXECUTE FUNCTION before_insert();
''').format(table=sql.Identifier(schema_name_in_db, raw_mark_table_name_in_db))

with psycopg.connect('dbname=ai_project user=API_write_data \
password=1111') as conn:
    conn.execute(query_befor_insert)
    conn.execute(qurey_triger_before_insert)
