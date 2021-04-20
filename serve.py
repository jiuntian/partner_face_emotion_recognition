# Main entry point
# Start server here
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import model
import io
import base64
from PIL import Image
import faceDetect as detection

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f.filename == '':
        flash("Please select a file")
        return redirect(request.url)
    elif not allowed_file(f.filename):
        flash("Invalid file type")
        return redirect(request.url)
    # filename = secure_filename(f.filename)
    # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = Image.open(f)
    
    cv2_img = detection.cvt_PIL_to_cv2(img)
    cropedList = detection.cropFace(cv2_img, detection.detectFaceArea(cv2_img))

    # check number of detected face
    if len(cropedList) < 1:
        flash("No face detected")
        return redirect(request.url)
    
    # take only one cropped face
    img = detection.cvt_cv2_to_PIL(cropedList[0])

    data = io.BytesIO()
    img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    flash("Upload successfully.")
    out = model.predictImage(img)
    flash("The predicted emotion is " + out)
    return render_template('upload.html', img_data=encoded_img_data.decode('utf-8'))

# Code for displaying uploaded image, comment out for now since we are not saving it
# @app.route('/display/<filename>')
# def display_image(filename):
# 	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
