from io import BytesIO
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import uuid

from opencv.face_detection import detect_faces

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ztogmztwoooidl:86f933bc481e9db9b8cbc75919a4540931471f81e3a8b64a7b71d728c8985a46@ec2-44-205-41-76.compute-1.amazonaws.com:5432/df9pu1etl8bcgb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# image upload model
class Upload(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

    # detect faces
    def detect(self):
        img_str, faces_found = detect_faces(self.data)
        download = Download(id=self.id, filename=self.filename, faces_found=faces_found, data=img_str)
        db.session.add(download)
        db.session.commit()

# processed image model (rectangle around faces)
class Download(db.Model):
    id = db.Column(db.String, primary_key=True)
    filename = db.Column(db.String(50))
    faces_found = db.Column(db.Integer)
    data = db.Column(db.LargeBinary)

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_id = str(uuid.uuid4())[:8]
        upload = Upload(id=file_id, filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return jsonify({'Message': f'Uploaded {file.filename}', 'ID': file_id})

@app.route('/download/<upload_id>', methods=['GET'])
@cross_origin()
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    download = Download.query.filter_by(id=upload_id).first()
    if not download:
        upload.detect()
        download = Download.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(download.data), attachment_filename=download.filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
