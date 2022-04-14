from io import BytesIO

from flask import Flask, render_template, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy 
import random
import string
import os
import datatime
def random_num():
    return ''.join(random.choices(string.digits, k=5))
    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class Upload(db.Model):
    id = db.Column(db.String, default=random_num, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return render_template("newsucess.html", filename123=file.filename, fileid123=upload.id)
    return render_template('index.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True)

@app.route('/giftcard')
def giftcard():
    return render_template('giftcard.html')

@app.route('/code')
def downloadPage():
    return render_template('enterCode.html')

@app.route('/background.png')
def backgroundPNG():
    return render_template('background.jpg')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
app.run()

