import psycopg
from psycopg import sql


# Название схемы и таблиц
schema_name_in_db = 'workflow'
drawing_table_name_in_db = 'drawing_data'
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
query_triger_before_insert = sql.SQL('''
    CREATE OR REPLACE TRIGGER check_unique_before_insert
    BEFORE INSERT ON {table}
    FOR EACH ROW
    EXECUTE FUNCTION before_insert();
''').format(table=sql.Identifier(schema_name_in_db, raw_mark_table_name_in_db))

# SQL запрос на создание функции вычисления реальных координат
query_after_insert = sql.SQL('''
    CREATE OR REPLACE FUNCTION coordinate_conversion()
    RETURNS TRIGGER AS $$
    BEGIN
    -- Проверяет тип операции после которой выполняется
        IF TG_OP = 'INSERT' THEN
            -- Вставляет реальные координаты
            INSERT INTO {table_mark}
                (mark_id,
                x_1_final,
                y_1_final,
                x_2_final,
                y_2_final,
                class_id,
                plan_id)
            VALUES
                (NEW.mark_id,
                (NEW.x_1 / 20) + (SELECT x_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                (NEW.y_1 / 20) - (SELECT y_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                (NEW.x_2 / 20) + (SELECT x_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                (NEW.y_2 / 20) - (SELECT y_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                NEW.class_id,
                NEW.plan_id
                );
        ELSIF TG_OP = 'UPDATE' THEN
            -- Обновляет координаты
            UPDATE {table_mark}
            SET mark_id = NEW.mark_id,
                x_1_final = (NEW.x_1 / 20) + (SELECT x_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                y_1_final = (NEW.y_1 / 20) - (SELECT y_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                x_2_final = (NEW.x_2 / 20) + (SELECT x_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                y_2_final = (NEW.y_2 / 20) - (SELECT y_origin FROM {table_pln} WHERE plan_id = NEW.plan_id),
                class_id = NEW.class_id,
                plan_id = NEW.plan_id
            WHERE mark_id = OLD.id;
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
''').format(
    table_mark=sql.Identifier(schema_name_in_db, mark_table_name_in_db),
    table_pln=sql.Identifier(schema_name_in_db, drawing_table_name_in_db)
)

# SQL запрос на создания тригера после вставки строки, добавлять экземпляр
# в таблицу с реальными координатами
query_triger_after_insert = sql.SQL('''
    CREATE OR REPLACE TRIGGER add_results_to_final_tabel
    AFTER INSERT OR UPDATE ON {table}
        FOR EACH ROW
    EXECUTE FUNCTION coordinate_conversion();
''').format(table=sql.Identifier(schema_name_in_db, raw_mark_table_name_in_db))

# Подключение к датабейзу и выполнение запросов
with psycopg.connect('dbname=ai_project user=API_write_data \
password=1111') as conn:
    conn.execute(query_befor_insert)
    conn.execute(query_triger_before_insert)
    conn.execute(query_after_insert)
    conn.execute(query_triger_after_insert)
