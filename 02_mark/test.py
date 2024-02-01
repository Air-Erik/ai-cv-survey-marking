import psycopg
from psycopg import sql

schema_name_in_db = 'workflow'
mark_table_name_in_db = 'raw_mark_data'

query_unique = sql.SQL('''
DELETE FROM {table_raw_mark}
WHERE (x_1, y_1, x_2, y_2, image_name) IN (
    SELECT x_1, y_1, x_2, y_2, image_name
    FROM (
        SELECT
            x_1, y_1, x_2, y_2, image_name,
            ROW_NUMBER() OVER (PARTITION BY x_1, y_1, x_2, y_2, image_name ORDER BY (SELECT NULL)) AS row_num
        FROM {table_raw_mark}
    ) AS subquery
    WHERE row_num > 1
);
''').format(
    table_raw_mark=sql.Identifier(schema_name_in_db, mark_table_name_in_db)
)

with psycopg.connect('dbname=ai_project user=API_write_data \
password=1111') as conn:
    conn.execute(query_unique)
