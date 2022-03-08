from http import HTTPStatus
from flask import Flask, render_template, redirect, request, url_for, abort, flash
import data_manager
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def hello():
    questions_to_display = data_manager.display_latest_five_questions()
    return render_template("open_page.html", questions_to_display=questions_to_display)


@app.route("/search", methods=["GET", "POST"])
def display_searched_questions():
    if request.method == "GET":
        searched_word = request.args.get('q')
        selected_questions = data_manager.get_questions_by_word(searched_word)
        return render_template("search.html", selected_questions=selected_questions, headers=data_manager.search_headers, searched_word=searched_word)
    elif request.method == "POST":
        return redirect("/")


@app.route("/list", methods=["GET"])
def display_questions():
    questions = data_manager.get_question_list()
    comments = data_manager.get_comment_list()
    return render_template("list_questions.html", comments=comments, questions=questions, headers=data_manager.question_headers)


@app.route("/question/<int:question_id>")
def display_given_question(question_id: int):
    data_manager.update_view_count(question_id)
    question = data_manager.get_question_by_question_id(question_id)
    answer = data_manager.get_answer_list_by_question_id(question_id)
    comments = data_manager.get_comment_list_by_question_id(question_id)
    return render_template("display_question.html", comments=comments, question_id=question_id, question=question, answers=answer)


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    questions = data_manager.get_question_list()
    tags = data_manager.get_all_tags()
    if request.method == "POST":
        question_id = data_manager.create_new_id(questions)
        id_first = 1
        vote_number = 0
        view_number = 0
        submission_time = data_manager.get_time()
        title = request.form.get('title')
        message = request.form.get('message')
        image = request.files.get('file')
        image_filename = os.path.dirname(__file__) + '/static/images/' + secure_filename(image.filename)
        # save image is not working yet
        #image.save(image_filename)
        new_data = [submission_time, view_number, vote_number, title, message, id_first, image_filename]
        data_manager.add_question(new_data)
        return redirect('list')
    else:
        tag_names = []
        for tag in tags:
            tag_names.append(tag['name'])
        id_list = data_manager.get_all_ids(questions)
        question_id = int(max(id_list))
        return render_template('add_question.html', id=question_id, tags=tag_names)


@app.route("/shows/<order>/<order_by>")
def sort_questions(order, order_by):
    sorted_questions = data_manager.sort_questions(order_by, order)
    return render_template("list_questions.html", questions=sorted_questions, headers=data_manager.question_headers)


@app.route("/question/<int:question_id>/new-answer", methods=["GET", "POST"])
def post_an_answer(question_id: int):
    answers_to_question = []
    if request.method == 'POST':
        answers_to_question.append(question_id)
        message = request.form.get("message")
        answers_to_question.append(message)
        image = request.files.get('file')
        image_filename = os.path.dirname(__file__) + '/static/images/' + secure_filename(image.filename)
        # save image is not working yet
        #image.save(image_filename)
        answers_to_question = [question_id, message, image_filename]
        data_manager.add_answer(answers_to_question)
        return redirect(url_for("display_given_question", question_id=question_id))
    return render_template("post_answer.html", question_id=question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect("/list")


@app.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
def edit_a_question(question_id):
    result = data_manager.get_question_by_question_id(question_id)
    question_data = {}
    if request.method == 'POST':
        q_title = request.form.get("title")
        q_message = request.form.get("message")
        data_manager.update_question(q_title, q_message, question_id)
        return redirect(f'/question/{question_id}')
    else:
        question_data['id'] = result[0]['id']
        question_data['title'] = result[0]['title']
        question_data['message'] = result[0]['message']
        return render_template("update_question.html", question=question_data)


@app.route("/answer/<int:answer_id>/delete") 
def delete_an_answer(answer_id):
    question_id_dict_list = data_manager.delete_answer(answer_id)
    question_id = question_id_dict_list['question_id']
    return redirect(f"/question/{question_id}")


@app.route("/comment/<int:comment_id>/delete")
def delete_comment_from_question(comment_id):
    comments = data_manager.get_comment_list()
    for key in comments:
        if str(key['id']) == str(comment_id):
            question_id = key['question_id']
    data_manager.delete_a_comment_from_question(comment_id)
    return redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/vote_up", methods=["GET", "POST"])
@app.route("/question/<question_id>/vote_down", methods=["GET", "POST"])
def vote_on_questions(question_id):
    if request.method == "POST":
        vote = 0
        if request.form.get("vote-up") == "up":
            vote = 1
        elif request.form.get("vote-down") == "down":
            vote = -1
        data_manager.update_question_vote_count(vote, question_id)
        return redirect("/list")


@app.route('/<tag_name>/tagged-questions')
def list_tagged_questions(tag_id):
    tagged_ids = data_manager.get_tagged_question_ids(tag_id)
    tagged_questions = []
    for value in tagged_ids.values():
        tagged_questions.append(data_manager.get_tagged_questions(value))


def display_current_tags():
    tags = request.form
    current_tags = []
    for tag in tags:
        current_tags.append(tag)
    return current_tags


@app.route("/answer/<int:answer_id>/vote")
def vote_on_answers():
    pass


@app.route("/question/<int:question_id>/new-comment", methods=["POST", "GET"])
def post_comment_to_q(question_id):
    if request.method == 'GET':
        question = data_manager.get_question_list()
        for row in question:
            if str(row['id']) == str(question_id):
                this_question = row['title']
                this_question_id = row['id']
    else:
        question_id = request.form.get('q_id')
        comment = request.form.get('comment')
        time = data_manager.get_time()
        data_manager.post_comment_to_q(question_id, comment, time)
        return redirect(f'/question/{question_id}')
    return render_template('post_question_comment.html', question_id=question_id,question=this_question,q_id=this_question_id)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )
