from flask import Flask, render_template, request, jsonify
import pyodbc

app = Flask(__name__) # Ініціалізація Flask

def get_db_connection(): # Налаштування підключення до SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-CH9S0JF\SQL2022SERVER;"
        "DATABASE=book_recommendations;"
        "UID=bookuser;"
        "PWD=01052004"
    )
    conn = pyodbc.connect(conn_str) # з'єднання з базою даних
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json # Отримання JSON даних із запиту від клієнта
    selected_genre = data.get('genre')
    selected_period = data.get('period')
    selected_country = data.get('countries', [])

    query = "SELECT title, author FROM books WHERE 1=1"
    params = []

    # Додавання умов атрибутів
    if selected_genre:
        query += " AND LOWER(genre) = LOWER(?)"
        params.append(selected_genre)
    if selected_period:
        query += " AND period = ?"
        params.append(selected_period)
    if selected_country:
        query += " AND LOWER(country) IN ({})".format(','.join(['?'] * len(selected_country)))
        params.extend(selected_country)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = [{'title': row[0], 'author': row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify({'recommendations': results}) # Повернення результатів у форматі JSON

if __name__ == '__main__':
    app.run(debug=True)