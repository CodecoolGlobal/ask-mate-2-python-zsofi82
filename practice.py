"""from flask import Flask, render_template, request, abort
from http import HTTPStatus

# [...]

@app.route('/question/create', methods=['GET', 'POST'])
def question():
    try:
        # RENDER EMPTY FORM, STATUS: 200
        if 'GET' == request.method:
            return render_template('question_create.html'), HTTPStatus.OK
        # RECEIVE AND PROCESS FORM DATA, STATUS: 201
        elif 'POST' == request.method:
            data_manager.create_question(request.form)
            return render_template('question_create.html'), HTTPStatus.CREATED
        # NOT ALLOWED METHOD, STATUS: 405
        else:
            abort(HTTPStatus.METHOD_NOT_ALLOWED)
    # IN CASE OF ANY ERROR, STATUS: 500
    except Exception as e:
        return render_template('error.html', message=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR"""