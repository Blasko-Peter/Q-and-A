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


@connection.connection_handler
def sql_add(cursor, subtime, title, msg, img):
    cursor.execute("""
                      INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                      VALUES (%s, 0, 0, %s, %s, %s);
    """, (subtime, title, msg, img))


@connection.connection_handler
def sql_search(cursor, keywords):
    keywords = "%" + keywords + "%"
    query = """SELECT id, title, submission_time, vote_number FROM question
               WHERE title ILIKE %(keyword)s OR message ILIKE %(keyword)s OR id IN
              (SELECT question_id FROM answer WHERE message ILIKE %(keyword)s)"""
    cursor.execute(query, {'keyword': keywords})
    result = cursor.fetchall()
    return result


@connection.connection_handler
def sql_display_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question 
                    WHERE id = %(question_id)s;
                    """, {'question_id': question_id})
    display = cursor.fetchall()
    return display


@connection.connection_handler
def sql_display_answer(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer 
                    WHERE question_id = %(question_id)s ORDER BY submission_time DESC;
                    """, {'question_id': question_id})
    display = cursor.fetchall()
    return display


@connection.connection_handler
def sql_display_comment_to_answer(cursor):
    cursor.execute("""
                    SELECT * FROM comment;
                    """,)
    display = cursor.fetchall()
    return display


@connection.connection_handler
def sql_get_question_comments(cursor, question_id):
    cursor.execute("""
                    SELECT * From comment 
                    WHERE question_id = %(question_id)s;
                    """, {'question_id': question_id})
    display = cursor.fetchall()
    return display
