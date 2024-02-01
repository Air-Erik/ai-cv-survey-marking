import psycopg
from psycopg import sql

schema_name_in_db = 'workflow'
mark_table_name_in_db = 'raw_mark_data'

query_unique = sql.SQL('''
    SELECT DISTINCT
        image_name
    FROM {table_raw_mark}
''').format(
    table_raw_mark=sql.Identifier(schema_name_in_db, mark_table_name_in_db)
)

with psycopg.connect('dbname=ai_project user=API_write_data \
password=1111') as conn:
    conn.execute(query_unique)
