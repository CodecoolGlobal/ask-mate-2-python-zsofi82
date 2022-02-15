from flask import Flask, render_template, redirect, request, url_for
import data_manager
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("open_page.html")


# missing: The questions are sorted by most recent.
@app.route("/list", methods=["GET", "POST"])
def display_questions():
    data_file = data_manager.question_file_path
    questions = connection.get_data_from_csv(data_file)
    return render_template("list_questions.html", questions=questions, headers=data_manager.question_headers)


@app.route("/question/<question_id>", methods=["GET", "POST"])
def display_a_question_with_answers(question_id):
    # if request.method == "GET":
    #     questions = connection.get_data_from_csv(data_manager.question_file_path)
    #     question_to_display = questions[question_id]
    #     answers_to_a_question = data_manager.get_answers_to_a_question
    #     answers = connection.get_data_from_csv(data_file)
    #     actual_answers = []
    #     for answer in answers:
    #         if str(question_id) == answer["question_id"]:
    #             actual_answers.append(answer)
    # return render_template("display_question.html", question=question_to_display, actual_answers=actual_answers)
    pass


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    pass


# @app.route("/question/<question_id>/new-answer")
# def post_an_answer():
#     pass
#
#
# @app.route("/question/<question_id>/delete")
# def delete_question():
#     pass
#
#
# @app.route("/question/<question_id>/edit")
# def edit_a_question():
#     pass
#
#
# @app.route("/answer/<answer_id>/delete")
# def delete_an_answer():
#     pass


# @app.route("/question/<question_id>/vote")
# def vote_on_questions():
#     pass


# @app.route("/answer/<answer_id>/vote")
# def vote_on_answers():
#     pass


if __name__ == "__main__":
    app.run()
