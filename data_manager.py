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


@connection.connection_handler
def sql_delete(cursor, id):
    cursor.execute("""
                      DELETE FROM question
                      WHERE id = %(id)s;
                      """, {'id': id})


@connection.connection_handler
def sql_update(cursor, question_id, subtime, title, msg, img):
    cursor.execute("""
                      UPDATE question
                      SET submission_time = %(subtime)s, view_number = '0', vote_number = '0', title = %(title)s, message = %(msg)s, image = %(img)s
                      WHERE id = %(question_id)s;
                """, {'subtime': subtime, 'title': title, 'msg': msg, 'img': img, 'question_id': question_id})


@connection.connection_handler
def sql_post_answer(cursor, subtime, question_id, msg, img):
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%s, 0, %s, %s, %s);
    """, (subtime, question_id, msg, img))


@connection.connection_handler
def sql_display_actual_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer 
                    WHERE id = %(answer_id)s;
                    """, {'answer_id': answer_id})
    display = cursor.fetchall()
    return display


@connection.connection_handler
def sql_update_answer(cursor, answer_id, subtime, msg):
    cursor.execute("""
                    UPDATE answer
                    SET submission_time = %(subtime)s, message = %(msg)s
                    WHERE id = %(answer_id)s;
    """, {'subtime': subtime, 'msg': msg, 'answer_id': answer_id})


@connection.connection_handler
def sql_delete_answer(cursor, answer_id):
    cursor.execute("""
                      DELETE FROM answer
                      WHERE id = %(answer_id)s;
                      """, {'answer_id': answer_id})


@connection.connection_handler
def sql_add_comment_to_question(cursor, question_id, message, submission_time):
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, NULL , %(message)s, %(submission_time)s, 0);
    """, {'question_id': question_id, 'message': message, 'submission_time': submission_time})


@connection.connection_handler
def sql_comdel(cursor, comment_id):
    cursor.execute("""
                        DELETE FROM comment
                        WHERE id = %(comment_id)s ;""", {'comment_id':comment_id})


@connection.connection_handler
def question_or_answer(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment WHERE id = %(comment_id)s;""",
                   {'comment_id':comment_id})
    display = cursor.fetchone()
    return display


@connection.connection_handler
def get_question_id(cursor, comment_id):
    cursor.execute("""
                    SELECT answer.question_id FROM answer
                    INNER JOIN comment
                    ON answer.id = comment.answer_id
                    WHERE comment.id = %(comment_id)s;
                    """, {'comment_id':comment_id})
    display = cursor.fetchone()
    return display


@connection.connection_handler
def get_comment_data(cursor, comment_id):
    cursor.execute("""
                    SELECT * From comment 
                    WHERE id = %(comment_id)s;
                    """, {'comment_id': comment_id})
    display = cursor.fetchall()
    return display


@connection.connection_handler
def sql_comment_edit(cursor, comment_id, msg):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(msg)s, edited_count = edited_count + 1
                    WHERE id = %(comment_id)s;
    """, {'msg': msg, 'comment_id': comment_id})
