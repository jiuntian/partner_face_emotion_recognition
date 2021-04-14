# Main entry point
# Start server here
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

@app.route("/")
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            flash("Please select a file")
            return render_template('index.html')
        elif not allowed_file(f.filename):
            flash("Invalid file type")
            return render_template('index.html')
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        return 'file uploaded successfully'
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
