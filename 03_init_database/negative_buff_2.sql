-- Основной SELECT запрос для извлечения идентификаторов линий и соответствующих отфильтрованных геометрий
SELECT 
    pd.line_id, 
    -- Собираем все линии, не пересекающиеся с буфером, обратно в мультилинию
    ST_Collect(sub.line) AS filtered_line_pipe
FROM 
    workflow.pipe_data AS pd  -- Работаем с данными по линиям

-- Подзапрос для разделения мультилиний на отдельные линии
JOIN (
    SELECT 
        line_id, 
        (ST_Dump(line_pipe)).geom AS line  -- Разбиваем каждую мультилинию на индивидуальные линии
    FROM 
        workflow.pipe_data
) AS sub ON pd.line_id = sub.line_id  -- Соединяем индивидуальные линии с их исходными ID

-- Левое соединение с буфером, созданным из геометрии полигонов, для проверки пересечений
LEFT JOIN (
    SELECT 
        ST_Buffer(pipe, -0.005) AS geom  -- Создаем внутренний буфер для каждого полигона
    FROM 
        workflow.raw_pipe_data
) AS buff ON ST_Crosses(sub.line, buff.geom)  -- Проверяем, пересекает ли линия буфер

-- Фильтруем результаты, чтобы оставить только линии, не пересекающиеся с буфером
WHERE 
    buff.geom IS NULL

-- Группируем результаты по line_id, чтобы каждый ID был представлен одной мультилинией
GROUP BY 
    pd.line_id;
