from flask import Flask
app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'app/static/images/upload'
app.secret_key = "keep it secret, keep it safe"