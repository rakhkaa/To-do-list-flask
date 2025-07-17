from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File untuk menyimpan data
DATA_FILE = 'todos.json'

def load_todos():
    """Load todos dari file JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Simpan todos ke file JSON"""
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def index():
    """Halaman utama menampilkan daftar todos"""
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    """Tambah todo baru"""
    task = request.form.get('task')
    if task:
        todos = load_todos()
        # Buat ID sederhana berdasarkan panjang list
        new_id = len(todos) + 1
        todos.append({
            'id': new_id,
            'task': task,
            'completed': False
        })
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Hapus todo berdasarkan ID"""
    todos = load_todos()
    todos = [todo for todo in todos if todo['id'] != todo_id]
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    """Toggle status completed todo"""
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Buat folder templates jika belum ada
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)
