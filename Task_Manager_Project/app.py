from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=False)
    last_updated_by = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    query = request.args.get('query')
    if query:
        tasks = Task.query.filter(Task.title.contains(query) | Task.status.contains(query)).all()
    else:
        tasks = Task.query.order_by(Task.due_date).all()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task = Task(
            title=request.form['title'],
            description=request.form['description'],
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d'),
            status=request.form['status'],
            remarks=request.form['remarks'],
            created_by=request.form['created_by'],
            last_updated_by=request.form['created_by']
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_task.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        task.status = request.form['status']
        task.remarks = request.form['remarks']
        task.last_updated_by = request.form['last_updated_by']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
