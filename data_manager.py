import os
import connection
from datetime import datetime, timedelta
import time
import server

dtime = datetime.now() + timedelta(seconds=3)
unixtime = time.mktime(dtime.timetuple())

QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
question_headers = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image"]
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
answer_headers = ["Id", "Submission time", "Vote number", "Question ID", "Message", "Image"]
search_headers = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image", "Answers"]


def get_time():
    return time.strftime("%F %H:%M:%S", time.localtime())


def get_all_ids(given_list):
    all_ids = [0]
    for given_list_dict in given_list:
        for key, value in given_list_dict.items():
            if key == "id":
                all_ids.append(int(value))
    return all_ids


def create_new_id(given_list):
    id_list = get_all_ids(given_list)
    new_id = int(max(id_list)) + 1
    return new_id


@connection.connection_handler
def add_question(cursor, new_data):
    query = f"""
        INSERT INTO question (submission_time,view_number,vote_number,title,message,image)
        VALUES('{new_data[0]}','{new_data[1]}','{new_data[2]}','{new_data[3]}','{new_data[4]}','{new_data[5]}')"""
    cursor.execute(query)
    return cursor.statusmessage


@connection.connection_handler
def get_question_list(cursor):
    query = """
        SELECT * FROM question
        ORDER BY submission_time DESC;"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_question_id(cursor, question_id):
    query = """
            SELECT *
            FROM question
            WHERE id = %(question_id)s;"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def get_questions_by_word(cursor, word):
    query = """
        SELECT DISTINCT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message AS q_message, question.image, answer.message AS a_message
        FROM question  
        LEFT JOIN answer
        ON question.id = answer.question_id
        WHERE
            question.title LIKE %(word)s OR
            question.message LIKE %(word)s OR
            answer.message LIKE %(word)s;"""
    cursor.execute(query, {'word': '%' + str(word) + '%'})
    return cursor.fetchall()


@connection.connection_handler
def update_question_vote_count(cursor, count, question_id):
    cursor.execute("""UPDATE question SET vote_number = vote_number + %s WHERE id = %s""",
                    (count, question_id))


@connection.connection_handler
def get_answer_list(cursor):
    query = """
            SELECT *
            FROM answer
            ORDER BY submission_time DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
                SELECT question_id
                FROM answer
                WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def get_answer_list_by_question_id(cursor, question_id):
    query = """
            SELECT *
            FROM answer
            WHERE question_id = %(question_id)s;"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_question(cursor, question_id):
    query = f"""
            DELETE FROM question
            WHERE id = {question_id};
            """
    cursor.execute(query)


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
            DELETE FROM answer
            WHERE id = %(answer_id)s
            RETURNING question_id;
            """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def update_question_vote_count(cursor, count, question_id):
    cursor.execute("""UPDATE question SET vote_number = vote_number + %s WHERE id = %s""",
                    (count, question_id))


@connection.connection_handler
def update_view_count(cursor, question_id):
    cursor.execute("""UPDATE question
                    SET view_number = view_number+1
                    WHERE id = %(question_id)s
                    """,{'question_id':question_id})


@connection.connection_handler
def update_question(cursor, title, message, question_id):
    query = f"""
            UPDATE question
            SET title = '{title}', message ='{message}'
            WHERE id = {question_id};"""
    cursor.execute(query)


@connection.connection_handler
def get_answer_id(cursor):
    inc_id = 1
    query = """
            SELECT id FROM answer
            ORDER BY id DESC LIMIT 1;"""
    cursor.execute(query)
    for id in cursor.fetchall():
        result = id["id"]
    result += inc_id
    return result


@connection.connection_handler
def execute_query_string_base(cursor, query_string):
    query = query_string
    cursor.execute(query)


@connection.connection_handler
def add_answer(cursor, form_data):
    query = f"""INSERT INTO answer (id, submission_time, vote_number, question_id, message, image)
                    VALUES (DEFAULT,DEFAULT,0, %s, %s, %s)
                    RETURNING *"""
    cursor.execute(query, form_data)
    return cursor.fetchall()


@connection.connection_handler
def sort_questions(cursor, order_by, order):
    query = sql.SQL("""
        SELECT *
        FROM question
        ORDER BY {order_by} {order};""").format(order=sql.Identifier(order), order_by=sql.Identifier(order_by))
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def display_latest_five_questions(cursor):
    query = """ SELECT * FROM question ORDER BY submission_time DESC limit 5"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_a_comment_from_question(cursor, comment_id):
    query = """ DELETE FROM comment WHERE id=%(comment_id)s RETURNING question_id"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@connection.connection_handler
def delete_a_comment_from_answer(cursor, comment_id):
    query = """ DELETE FROM comment WHERE id=%(comment_id)s RETURNING answer_id"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@connection.connection_handler
def get_all_tags(cursor):
    query = """SELECT name FROM tag ORDER BY name"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tagged_question_ids(cursor, tag_id):
    query = """SELECT question_id FROM question_tag WHERE tag_id=%(tag_id)s"""
    cursor.execute(query, {'tag_id': tag_id})
    return cursor.fetchall()


@connection.connection_handler
def get_tagged_questions(cursor, tagged_id):
    query = """SELECT * FROM question WHERE id=%(tagged_id)s"""
    cursor.execute(query, {'tagged_id': tagged_id})
    return cursor.fetchall()


@connection.connection_handler
def get_tag(cursor, tag_name):
    query = """SELECT * FROM tag WHERE name=%(tag_name)s"""
    cursor.execute(query, {'tag_name': tag_name})
    return cursor.fetchall()


@connection.connection_handler
def give_tag_to_question(cursor, question_id: int, tag_id: int):
    query = """INSERT INTO question_tag VALUES (%(question_id)s, %(tag_id)s)"""
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})
    return cursor.fetchall()


@connection.connection_handler
def get_image_path(cursor, question_id):
    query = """SELECT image FROM question WHERE id=%(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@connection.connection_handler
def post_comment_to_q(cursor, question_id, message, sm_time):
    query = f"""
            INSERT INTO comment (question_id, message, submission_time)
            VALUES ({question_id},'{message}','{sm_time}');"""
    cursor.execute(query)


@connection.connection_handler
def get_comment(cursor):
    query = """
            SELECT *
            FROM comment"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comment_list_by_question_id(cursor, question_id):
    query = f"""
            SELECT *
            FROM comment
            WHERE question_id = {question_id}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comment_list(cursor):
    query = f"""
            SELECT *
            FROM comment
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def delete_a_comment_of_question(cursor,question_id):
    query = f"""
            DELETE FROM comment
            WHERE question_id = {question_id};"""
    cursor.execute(query)


@connection.connection_handler
def delete_question_tag_of_question(cursor,question_id):
    query = f"""
            DELETE FROM question_tag
            WHERE question_id = {question_id};"""
    cursor.execute(query)


@connection.connection_handler
def delete_an_answer_of_question(cursor,question_id):
    query = f"""
            DELETE FROM answer
            WHERE question_id = {question_id};"""
    cursor.execute(query)
