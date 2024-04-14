from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Using SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a simple model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    author = db.Column(db.String(50))
    overview = db.Column(db.String(200))
    image = db.Column(db.String(200))
    url = db.Column(db.String(100))

# Define a function to initialize the database
def init_db():
    with app.app_context():
        db.create_all()

# Check if the database needs initialization
if not os.path.exists('site.db'):
    init_db()

@app.route('/')
def hello_world():
    query = request.args.get('query')
    if query:
        courses = Course.query.filter(Course.title.contains(query)) or Course.overview.contains(query)
    else:
        courses = Course.query.all()
    return render_template('courseview.html', course=courses)


@app.route('/loaddata')
def loaddata():
    data = Course.query.all()

    if(len(data) == 0):
        #create load from json
        with open('courses.json') as f:
            courses = json.load(f)
            for course in courses:
                new_course = Course(title=course['title'], 
                                    author=course['author'], 
                                    overview=course['overview'], 
                                    image=course['img'], 
                                    url=course['url'])
                db.session.add(new_course)
                db.session.commit()
        return "Courses loaded successfully"

if __name__ == '__main__':
    app.run(debug=True)
