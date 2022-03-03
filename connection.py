import csv
import time
import data_manager
import database_common
#from practice import question

import server


def get_data_from_csv(csvfile):
    with open(csvfile, "r") as csv_file:
        data = []
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
        return data


def write_data_to_csv(csvfile, given_list, data_header):
    with open(csvfile, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writeheader()
        for row in given_list:
            csv_writer.writerow(row)


def update_data_in_csv(csvfile, updated_data, given_list, data_header):
    the_exception = data_manager.QUESTION_HEADER[1],data_manager.QUESTION_HEADER[2],data_manager.QUESTION_HEADER[3],data_manager.QUESTION_HEADER[6]
    for existing_dict in given_list:
        for key, value in existing_dict.items():
            if int(updated_data["id"]) == int(existing_dict["id"]):
                if key not in the_exception:
                    existing_dict[key] = updated_data[key]
    write_data_to_csv(csvfile, given_list, data_header)


def delete_from_csv(csv_file, given_id, given_list, header):
    new_list = []
    for data_dict in given_list:
        if int(data_dict["id"]) != int(given_id):
            new_list.append(data_dict)
    write_data_to_csv(csv_file, new_list, header)
    return new_list


def get_time():
    return time.strftime("%F %H:%M:%S", time.localtime())


def update_csv(file_to_rewrite, updated_dict_list):
    with open(file_to_rewrite, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_manager.QUESTION_HEADER)
        writer.writeheader()
        for row in updated_dict_list:
            writer.writerow(row)


@database_common.connection_handler
def add_question(cursor, new_data):
    query = f"""
        INSERT INTO question (submission_time,view_number,vote_number,title,message,image)
        VALUES('{new_data[0]}','{new_data[1]}','{new_data[2]}','{new_data[3]}','{new_data[4]}','{new_data[5]}')"""
    cursor.execute(query)
    return cursor.statusmessage


@database_common.connection_handler
def get_question_list(cursor):
    query = """
        SELECT * FROM question
        ORDER BY submission_time DESC;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_question_id(cursor, question_id):
    query = """
            SELECT *
            FROM question
            WHERE id = %(question_id)s;"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_by_word(cursor, word):
    query = """
        SELECT DISTINCT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image
        FROM answer, comment, question
        WHERE 
            question.title LIKE %(word)s OR 
            question.message LIKE %(word)s OR 
            answer.message LIKE %(word)s
        ORDER BY question.vote_number;"""
    cursor.execute(query, {'word': '%' + str(word) + '%'})
    return cursor.fetchall()


@database_common.connection_handler
def update_question_vote_count(cursor, count, question_id):
    cursor.execute("""UPDATE question SET vote_number = vote_number + %s WHERE id = %s""",
                    (count, question_id))


@database_common.connection_handler
def get_answer_list(cursor):
    query = """
            SELECT *
            FROM answer
            ORDER BY submission_time DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """
                SELECT question_id
                FROM answer
                WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_list_by_question_id(cursor, question_id):
    query = """
            SELECT *
            FROM answer
            WHERE question_id = %(question_id)s;"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = f"""
            DELETE FROM question
            WHERE id = {question_id};
            """
    cursor.execute(query)
    print('hello')


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    query = """
            DELETE FROM answer
            WHERE id = %(answer_id)s
            RETURNING question_id;
            """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in server.ALLOWED_EXTENSIONS


@database_common.connection_handler
def update_question_vote_count(cursor, count, question_id):
    cursor.execute("""UPDATE question SET vote_number = vote_number + %s WHERE id = %s""",
                    (count, question_id))


@database_common.connection_handler
def update_view_count(cursor, question_id):
    cursor.execute("""UPDATE question
                    SET view_number = view_number+1
                    WHERE id = %(question_id)s
                    """,{'question_id':question_id})


@database_common.connection_handler
def update_question(cursor, title, message, question_id):
    query = f"""
            UPDATE question
            SET title = '{title}', message ='{message}'
            WHERE id = {question_id};"""
    cursor.execute(query)


@database_common.connection_handler
def get_answer_id(cursor):
    inc_id = 1
    query = """
            SELECT id FROM answer
            ORDER BY id DESC LIMIT 1;"""
    cursor.execute(query)
    for id in cursor.fetchall():
        result=id["id"]
    result += inc_id
    return result


@database_common.connection_handler
def execute_query_string_base(cursor, query_string):
    query = query_string
    cursor.execute(query)


@database_common.connection_handler
def add_answer(cursor, form_data):
    query = f"""INSERT INTO answer (id, submission_time, vote_number, question_id, message, image)
                    VALUES (DEFAULT,DEFAULT,0, %s, %s, %s)
                    RETURNING *"""
    cursor.execute(query, form_data)
    return cursor.fetchall()


def sort_questions(cursor, order_by, order):
    query = """
        SELECT *
        FROM question
        ORDER BY %(order_by)s %(order)s;"""
    cursor.execute(query, {'order_by': order_by, 'order': order})
    return cursor.fetchall()


@database_common.connection_handler
def display_latest_five_questions(cursor):
    query = """ SELECT * FROM question ORDER BY submission_time DESC limit 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_a_comment_from_question(cursor, comment_id):
    query = """ DELETE FROM comment WHERE id=%(comment_id)s RETURNING question_id"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@database_common.connection_handler
def delete_a_comment_from_answer(cursor, comment_id):
    query = """ DELETE FROM comment WHERE id=%(comment_id)s RETURNING answer_id"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()

@database_common.connection_handler
def post_comment_to_q(cursor, question_id,message,time):
    query = f"""
            INSERT INTO comment (question_id, message, submission_time)
            VALUES ({question_id},'{message}','{time}');"""
    cursor.execute(query)
