import os
from flask import Flask, flash, request, redirect, url_for,send_from_directory,render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

if not os.path.exists('uploads'):
    os.mkdir('uploads')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download_file',methods=['GET','POST'])
def download_file():
    if request.method=='GET':
        fname=request.args.get('name')
        return fname


@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def downloads(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    return send_from_directory(uploads,filename,as_attachment=True)


@app.route('/myfile')
def myfile():
    return render_template('download.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
