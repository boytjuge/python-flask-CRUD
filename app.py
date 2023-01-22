from flask import Flask,redirect,render_template,url_for,jsonify,request,make_response
#from allfunction import  users
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/dapp'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))
    done = db.Column(db.Boolean)
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done
        }

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'active': self.active
        }        


# @app.route('/<int:id>')
# def index(id):
#     data = users.Users.getAllUser()
#     return data

# @app.route('/<name>',methods=["GET"])
# def recive(name):
#     return jsonify({"name":name})


@app.route('/tasks', methods=['GET', 'POST'])
def all_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return  jsonify([task.serialize() for task in tasks])
    elif request.method == 'POST':
        data = request.get_json()
        task = Task(title=data['title'], description=data['description'], done=data['done'])
        db.session.add(task)
        db.session.commit()
        return jsonify(task.serialize())

@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def task_by_id(id):
    task = Task.query.get(id)
    if request.method == 'GET':
        if task is None:
            return jsonify({'error': 'Task not found'})
        return jsonify(task.serialize())
    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.description = data['description']
        task.done = data['done']
        if task is None:
            return jsonify({'error': 'Task not found'})
        db.session.commit()
        return jsonify(task.serialize())
    elif request.method == 'DELETE':
        if task is None:
            return jsonify({'error': 'Task not found'})
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1",port=5500,debug=True)