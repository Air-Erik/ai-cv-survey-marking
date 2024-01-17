import psycopg
from psycopg import sql

schema_name_in_db = 'workflow'
table_name_in_db = 'classes'

query_return = sql.SQL('''
    SELECT class FROM {}
    ''').format(sql.Identifier(schema_name_in_db, table_name_in_db))

with psycopg.connect('dbname=ai_project user=API_write_data \
password=1111') as conn:
    record = conn.cursor().execute(query_return).fetchall()
    class_names_in_db = [i[0] for i in record]

print(class_names_in_db)
