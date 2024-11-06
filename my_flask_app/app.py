from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Викликаємо функцію для ініціалізації бази даних
init_db()

# Головна сторінка з формами реєстрації та авторизації
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')  # Перевіряємо, яку дію вибрав користувач

        username = request.form['username']
        password = request.form['password']
        
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            if action == 'register':
                # Реєстрація користувача
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    return "Реєстрація успішна! Тепер увійдіть у систему."
                except sqlite3.IntegrityError:
                    return "Користувач з таким іменем вже існує"
            elif action == 'login':
                # Авторизація користувача
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()
                if user:
                    session['username'] = username
                    return f"Успішний вхід! Вітаємо, {session['username']}!"
                else:
                    return "Невірний логін або пароль"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

