from flask import Flask, render_template, redirect, request
import data_manager
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/list")
def display_questions():
    data_file = data_manager.quesiton_file_path
    questions = connection.get_data_from_csv(data_file)
    return render_template("list_questions.html", questions=questions, headers=data_manager.question_headers)


# @app.route("/question/<question_id>")
# def display_a_question():
#     pass
#
#
# @app.route("/add-question")
# def add_a_question():
#     pass
#
#
# @app.route("/question/<question_id>/new-answer")
# def post_an_answer():
#     pass
#
#
# @app.route("/question/<question_id>/delete")
# def post_an_answer():
#     pass
#
#
# @app.route("/question/<question_id>/edit")
# def post_an_answer():
#     pass
#
#
# @app.route("/answer/<answer_id>/delete")
# def post_an_answer():
#     pass


if __name__ == "__main__":
    app.run()
