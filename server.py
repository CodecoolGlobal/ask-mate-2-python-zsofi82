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
    rev_questions = reversed(questions)  # To sort the questions by most recent.
    return render_template("list_questions.html", questions=rev_questions, headers=data_manager.question_headers)


@app.route("/question/<int:question_id>", methods=["GET", "POST"])
def update_given_question(question_id):
    if request.method == "GET":
        questions = connection.get_data_from_csv(data_manager.question_file_path)
        question_id = int(question_id)-1
        question_to_display = questions[question_id]
        answers_to_a_question = data_manager.get_answers_to_a_question(question_id)
        return render_template("update_question.html", question_id=question_id, question=question_to_display, answers=answers_to_a_question)
    else:
        return redirect("/list")


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        question_csv_file = data_manager.question_file_path
        questions = connection.get_data_from_csv(question_csv_file)
        question = {}
        for key in data_manager.QUESTION_HEADER:
            question[key] = request.form.get(key)
        question["id"] = data_manager.create_new_id(questions)
        connection.write_data_to_csv(csvfile=question_csv_file, new_data_dict=question, given_list=questions, data_header=data_manager.QUESTION_HEADER)
        return redirect('list')
    else:
        return render_template('add_question.html')


# @app.route("/question/<question_id>/new-answer")
# def post_an_answer():
#     pass
#
#
# @app.route("/question/<question_id>/delete")
# def delete_question():
#     pass


@app.route("/question/<int:question_id>/edit")
def edit_a_question(question_id):
    pass


# @app.route("/answer/<int:answer_id>/delete")
# def delete_an_answer():
#     pass


# @app.route("/question/<int:question_id>/vote")
# def vote_on_questions():
#     pass


# @app.route("/answer/<int:answer_id>/vote")
# def vote_on_answers():
#     pass


if __name__ == "__main__":
    app.run()
