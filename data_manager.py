import os
import connection
from datetime import datetime, timedelta
import time

dtime = datetime.now() + timedelta(seconds=3)
unixtime = time.mktime(dtime.timetuple())

question_file_path = os.getenv('question_file_path') if 'question_file_path' in os.environ else os.path.dirname(os.path.abspath(__file__))+'/sample_data/question.csv'
QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
question_headers = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image"]
answer_file_path = os.getenv('answer_file_path') if 'answer_file_path' in os.environ else os.path.dirname(os.path.abspath(__file__))+'/sample_data/answer.csv'
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
answer_headers = ["Id", "Submission time", "Vote number", "Question ID", "Message", "Image"]
QUESTIONS = "sample_data/question.csv"
ANSWERS = "sample_data/answer.csv"


def get_answers_to_a_question(question_id):
    answers = connection.get_data_from_csv(answer_file_path)
    answers_to_a_question = []
    for answer in answers:
        if int(answer["question_id"]) == int(question_id):
            answers_to_a_question.append(answer)
    return answers_to_a_question


def get_a_question(question_id):
    questions = connection.get_data_from_csv(question_file_path)
    for question in questions:
        if int(question["id"]) == question_id:
            return question


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


def update_count(filename, list_to_update, selected_id, key, count):
    for row in list_to_update:
        if row['id'] == selected_id:
            result = row
            index = list_to_update.index(result)
            list_to_update.pop(index)
            result[key] = int(result[key])
            result[key] = result[key] + count
            list_to_update.insert(index, result)
            print(row)
            connection.update_csv(filename,list_to_update)
