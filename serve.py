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


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


@app.route("/")
def index():
    return render_template('main.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f.filename == '':
        flash("Please select a file")
        return index()  # redirect(request.url)
    elif not allowed_file(f.filename):
        flash("Invalid file type")
        return index()  # redirect(request.url)

    img = Image.open(f)
    
    cv2_img = detection.cvt_PIL_to_cv2(img)
    rectList = detection.detectFaceArea(cv2_img)

    # check number of detected face
    if len(rectList) < 1:
        flash("No face detected")
        return index()  # redirect(request.url)
    
    # crop images
    imgList = []
    for (x, y, w, h) in rectList:
        imgList.append(img.crop((x, y, x + w, y + h)))
    flash("Upload successfully.")

    img_data = []
    for img in imgList:
        data = io.BytesIO()
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())  # convert to base64 in byte
        img_data.append(encoded_img_data.decode('utf-8'))  # convert to base64 in utf-8

    out = model.predictImage(imgList)

    return render_template('main.html', img_data=img_data, res=out)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
