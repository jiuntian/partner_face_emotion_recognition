# Main entry point
# Start server here
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST'])
def upload_file():
    f = request.files['file']
    if f.filename == '':
        flash("Please select a file")
        return redirect(request.url)
    elif not allowed_file(f.filename):
        flash("Invalid file type")
        return redirect(request.url)
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash("Upload successfully.")
    return render_template('upload.html', filename=filename)
    
@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
