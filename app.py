from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# since I am extremely shite at web development, lets start simple then,
# see if I can embed YouTube videos on static website, then try with doing the database way

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)


class MusicWeb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # in sqlite, its data_created, no idea why,

    # but don't let it fool you, no matter what you named here, even "shabi" will give you data_created for some reason

    def __repr__(self):
        return '<Comment %r>' % self.id  # it's a bit like format string somehow %s also works


@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        data = MusicWeb.query.order_by(MusicWeb.date_created).all()
        return render_template('index.html', items=data)


@app.route('/<int:id>', methods=['GET'])
def tryout(id):
    theSong = MusicWeb.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('firstSong_test.html', item=theSong)


@app.route('/hidden-link/post-new', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        newSongName = request.form['name']
        newSongContent = request.form['content']
        newSong = MusicWeb(name=newSongName, content=newSongContent)
        try:
            db.session.add(newSong)
            db.session.commit()
            print('shabi')
            return redirect('/hidden-link/post-new')
        except:
            return 'Something wrong with posting new'

    else:
        return render_template('post.html')


@app.route('/hidden-link/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    theSong = MusicWeb.query.get_or_404(id)

    if request.method == 'POST':
        theSong.content = request.form['content']

        try:
            db.session.commit()
            return render_template('update.html', item=theSong)
        except:
            return 'sth went wrong with updating'

    else:
        return render_template('update.html', item=theSong)


if __name__ == '__main__':
    app.run()
