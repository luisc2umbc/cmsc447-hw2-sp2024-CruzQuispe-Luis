from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

#this will initate a table if one does not exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            points INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

#this is called anytime the app is launched
init_db()

#homepage
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('base.html', users=users)

#add user route
@app.route('/add_user')
def add_user_page():
    return render_template('add_user.html')

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    points = int(request.form['points'])
    user_id = int(request.form['id'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return redirect(url_for('add_user_page'))

    cursor.execute('INSERT INTO users (id, name, points) VALUES (?, ?, ?)', (user_id, name, points))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

#edit route
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        points = int(request.form['points'])
        new_id = int(request.form['id'])
        cursor.execute('UPDATE users SET id=?, name=?, points=? WHERE id=?', (new_id, name, points, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return render_template('edituser.html', user=user)

#delete user route
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

#user search
@app.route('/search', methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE name LIKE ?', ('%' + search_query + '%',))
        users = cursor.fetchall()
        conn.close()
        return render_template('search_results.html', users=users, search_query=search_query)
    else:
        return render_template('search_user.html')

if __name__ == '__main__':
    app.run()
