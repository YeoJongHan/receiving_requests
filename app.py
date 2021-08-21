from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'requests.db')

db = SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
def home():
    requests_list = Reqs.query.order_by(Reqs.id.desc())
    if request.method == 'POST':
        data = request.data
        req = Reqs(content=data)
        db.session.add(req)
        db.session.commit()
    return render_template('home.html', reqs=requests_list)


class Reqs(db.Model):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    content = Column(String)


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')