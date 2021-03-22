import os
from collections import namedtuple

from werkzeug.utils import secure_filename

import md5 as md5_file
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

directory = os.path.abspath(os.curdir)
message = ''
hash_message = ''
file_1, res_f1 = '', ''
file_2, res_f2 = '', ''
conclusion = ''


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    global message, hash_message
    message = request.form['text']
    hash_message = md5_file.start_md5(message)
    return redirect(url_for('hash_string'))


@app.route('/hash_string', methods=['GET'])
def hash_string():
    return render_template('hash-string.html', hash_message=hash_message, message=message)


@app.route('/hash_files', methods=['GET', 'Post'])
def hash_files():
    return render_template('hash-files.html', file_1=file_1, file_2=file_2, res_f1=res_f1,
                           res_f2=res_f2, conclusion=conclusion)


@app.route('/checksums', methods=['POST'])
def checksums():
    global file_1, file_2, res_f1, res_f2, conclusion
    file_1 = request.files['file_1']
    file_2 = request.files['file_2']

    for file in (file_1, file_2):
        filename = secure_filename(file.filename)
        file.save(os.path.join(directory, filename))

        with open(directory + '/' + filename, 'rb') as f:
            file_content = f.read()
            hash_file = md5_file.md5(file_content)
            if file == file_1:
                res_f1 = hash_file
            else:
                res_f2 = hash_file
    if res_f1 == res_f2:
        conclusion = "File checksums match"
    else:
        conclusion = "Checksums of files DO NOT match"

    return redirect(url_for('hash_files'))


if __name__ == '__main__':
    app.run(debug=True)