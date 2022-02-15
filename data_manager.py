import os
import connection
import csv


question_file_path = os.getenv('question_file_path') if 'question_file_path' in os.environ else 'sample_data/question.csv'
QUESTION_HEADER = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
question_headers = ["Id", "Submission time", "View number", "Vote number", "Title", "Message", "Image"]
answer_file_path = os.getenv('answer_file_path') if 'answer_file_path' in os.environ else 'sample_data/answer.csv'
ANSWER_HEADER = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
answer_headers = ["Id", "Submission time", "Vote number", "Question ID", "Message", "Image"]
