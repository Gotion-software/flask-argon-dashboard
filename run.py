import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from subprocess import call

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.abspath(app.config['UPLOAD_FOLDER'] + filename))
            cmd = 'scp -i gotion-ec2.pem ' + os.path.abspath(app.config['UPLOAD_FOLDER'] + filename + ' ubuntu@52.8.108.75:~/docker-airflow-1/manual_uploads'
            call(cmd.split())
            flash('Successfully uploaded file.')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
