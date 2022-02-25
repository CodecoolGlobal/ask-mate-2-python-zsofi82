from http import HTTPStatus
from flask import Flask, render_template, redirect, request, url_for, abort
import data_manager
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("open_page.html")


@app.route("/list", methods=["GET"])
def display_questions():
    data_file = data_manager.question_file_path
    questions = connection.get_data_from_csv(data_file)
    rev_questions = reversed(questions)  # To sort the questions by most recent.
    return render_template("list_questions.html", questions=rev_questions, headers=data_manager.question_headers)


@app.route("/question/<int:question_id>", methods=["GET"])
def display_given_question(question_id: int):
    if request.method == "GET":
        question_to_display = data_manager.get_a_question(question_id)
        answers_to_a_question = data_manager.get_answers_to_a_question(question_id)
        return render_template("display_question.html", question_id=question_id, question=question_to_display, answers=answers_to_a_question)
    else:
        return redirect("/list")


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    question_csv_file = data_manager.question_file_path
    questions = connection.get_data_from_csv(question_csv_file)
    if request.method == "POST":
        question_csv_file = data_manager.question_file_path
        questions = connection.get_data_from_csv(question_csv_file)
        question = {}
        for key in data_manager.QUESTION_HEADER:
            question[key] = request.form.get(key)
        question["id"] = data_manager.create_new_id(questions)
        questions.append(question)
        connection.write_data_to_csv(csvfile=question_csv_file, given_list=questions, data_header=data_manager.QUESTION_HEADER)
        return redirect('list')
    else:
        id_list = data_manager.get_all_ids(questions)
        question_id = int(max(id_list))
        return render_template('add_question.html', id=question_id)


@app.route("/shows/<order>/<order_by>")
def sort_questions(order, order_by):
    questions = connection.get_data_from_csv(data_manager.question_file_path)
    sorted_questions = sorted(questions, key=lambda h: h[order_by], reverse=(order == "desc"))
    return render_template("list_questions.html", order=order, questions=sorted_questions, headers=data_manager.question_headers)


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def post_an_answer(question_id: int):
    answer_csv_file_path = data_manager.answer_file_path
    answers = connection.get_data_from_csv(answer_csv_file_path)
    if request.method == "POST":
        new_answer = {}
        for key in data_manager.ANSWER_HEADER:
            new_answer[key] = request.form.get(key)
        new_answer['id'] = data_manager.create_new_id(answers)
        new_answer['question_id'] = question_id
        answers.append(new_answer)
        connection.write_data_to_csv(csvfile=answer_csv_file_path, given_list=answers, data_header=data_manager.ANSWER_HEADER)
        return redirect(url_for('display_given_question', question_id=question_id))
    else:
        return render_template('post_answer.html', question_id=question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id: int):
    question_csv_file = data_manager.question_file_path
    questions = connection.get_data_from_csv(question_csv_file)
    answer_csv_file = data_manager.answer_file_path
    answers_to_a_question = data_manager.get_answers_to_a_question(question_id)
    connection.delete_from_csv(csv_file=question_csv_file, given_id=question_id, given_list=questions, header=data_manager.QUESTION_HEADER)
    for answer in answers_to_a_question:
        answer_id = int(answer["id"])
        connection.delete_from_csv(csv_file=answer_csv_file, given_id=answer_id, given_list=answers_to_a_question,
                                   header=data_manager.ANSWER_HEADER)
    return redirect("/list")


@app.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_a_question(question_id: int):
    question_csv_file = data_manager.question_file_path
    questions = connection.get_data_from_csv(question_csv_file)
    updated_question = {}
    try:
        if request.method == "GET":
            for question in questions:
                if int(question["id"]) == question_id:
                    return render_template("update_question.html", question_id=question_id, question=question)
        elif request.method == "POST":
            for key in data_manager.QUESTION_HEADER:
                updated_question[key] = request.form.get(key)
            updated_question["id"] = question_id
            connection.update_data_in_csv(csvfile=question_csv_file, updated_data=updated_question, given_list=questions, data_header=data_manager.QUESTION_HEADER)
            return render_template("display_question.html", question_id=question_id, question=updated_question)
        else:
            abort(HTTPStatus.METHOD_NOT_ALLOWED)
            return None
    except Exception as e:
        return render_template('error.html', question_id=question_id), HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/answer/<int:answer_id>/delete")
def delete_an_answer(answer_id: int):
    answer_csv_file = data_manager.answer_file_path
    answers = connection.get_data_from_csv(answer_csv_file)
    question_id = 0
    for answer in answers:
        if int(answer["id"]) == answer_id:
            question_id = int(answer["question_id"])
    connection.delete_from_csv(csv_file=answer_csv_file, given_id=answer_id, given_list=answers, header=data_manager.ANSWER_HEADER)
    return redirect(f"/question/{question_id}")


@app.route("/question/<int:question_id>/vote")
def vote_on_questions():
    pass


@app.route("/answer/<int:answer_id>/vote")
def vote_on_answers():
    pass


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )
