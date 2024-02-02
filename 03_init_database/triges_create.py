
# SQL запрос на создание функции проверки строки на уникальность по  5 столбцам
'''
CREATE OR REPLACE FUNCTION before_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем наличие дубликатов перед вставкой
    IF EXISTS (
        SELECT 1
        FROM workflow.raw_mark_data
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
'''

# SQL запрос на создание тригера перед вставкой для проверки уникальности
'''
CREATE TRIGGER check_unique_before_insert
BEFORE INSERT ON workflow.raw_mark_data
FOR EACH ROW
EXECUTE FUNCTION before_insert();
'''
