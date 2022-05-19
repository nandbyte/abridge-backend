from flask import Flask,jsonify,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

import pickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///test.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/',methods =['POST','GET'])
def index():
    if(request.method == 'POST'):
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return "ok"


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html',task=task)

@app.route('/expredict',methods=['GET'])
def expredict():
    input_string = str(request.form.get("txt"))
    print(input_string)
    input_lst = []
    input_lst.append(input_string)
    summary_model = pickle.load(open("finalmodel.pkl", 'rb'))
    prediction = summary_model.predict(input_lst)
    print(prediction[0])
    return prediction[0]

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    input_string = request.form.get()
    
    input_lst = []

   
    
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
    CORS(app)