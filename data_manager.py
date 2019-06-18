import connection
from psycopg2 import sql


@connection.connection_handler
def sql_display(cursor):
    cursor.execute("""
                      SELECT id, title, submission_time, vote_number FROM question
                      ORDER BY submission_time DESC;""")
    display = cursor.fetchall()
    return display


@connection.connection_handler
def sql_display_limit(cursor, limit):
    cursor.execute("""
                      SELECT id, title, submission_time, vote_number FROM question
                      ORDER BY submission_time DESC LIMIT %s ;""", str(limit))
    display = cursor.fetchall()
    return display