from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connect_string='mongodb+srv://salmanananda:Amamcoy9*@cluster0.qajnlru.mongodb.net/?retryWrites=true&w=majority'
client=MongoClient(connect_string)
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['POST'])
def save_diary():
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profileName = f'profile-{mytime}.{extension}'
    save_to = f'static/{profileName}'
    profile.save(save_to)
    

    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    doc = {
    'file': filename,
    'profile': profileName,
    'time' : mytime,
    'title': title_receive,
    'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'msg':'Upload complete!'})

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)