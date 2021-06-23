from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////PYTHON/İleriKurs/KursProgramları/TodoApp/todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    completed = db.Column(db.Boolean)


    # def __repr__(self):
    #     return '<User %r>' % self.username

@app.route("/")
def index():
    alltodoList=Todo.query.all()
    return render_template("index.html", todos=alltodoList)

#yanlızca POST izin verildi GET izin verilmedi
@app.route("/add",methods=["POST"])
def addTodo():
 
    title=request.form.get("title")
    newTodo=Todo(title=title, completed=False)
    db.session.add(newTodo)
    db.session.commit()
    
    return redirect (url_for("index"))

@app.route("/todocomplete/<string:id>")
def todocomplete(id):
    #primary key olduğu için get kullanılabilir, 
    #yoksa Todo.querry.filter_by(id=id) şeklinde fltreleme yaparız
    todo=Todo.query.get(id)
    todo.completed=True
    db.session.commit()
    return redirect (url_for("index"))

@app.route("/tododelete/<string:id>")
def tododelete(id):
    todo=Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect (url_for("index"))


if __name__=="__main__":
    db.create_all()
    app.run(debug=True)