from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet

app = Flask(__name__)
key = Fernet.generate_key()

host = 'localhost'
port = 5432
dbname = 'EXAMEN_ON'
user = 'postgres'
password = 1234


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn


@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM computadora_on')
    users = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    procesador = new_user['procesador']
    costo = new_user['costo']
    marca = new_user['marca']
    numero = new_user['numero']


    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO computadora_on (procesador, costo, marca, numero) VALUES (%s, %s, %s, %s) RETURNING *',
                (procesador, costo, marca, numero  ))
    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_user)


@app.delete('/api/users/<id>')
def delete_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM computadora_on WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()

    conn.commit()

    conn.close()
    cur.close()

    if user is None:
        return jsonify({'message': 'User Not Found'}, 404)

    return jsonify(user)


@app.put('/api/users/<id>')
def update_users(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_user = request.get_json()
    procesador = new_user['procesador']
    costo = new_user['costo']
    marca = new_user['marca']
    numero = new_user['numero']
    cur.execute(
        'UPDATE computadora_on SET procesador = %s, costo = %s, marca = %s, numero = %s WHERE id = %s RETURNING *', (procesador, costo, marca, numero, id))
    update_user = cur.fetchone()
    
    conn.commit()
    
    conn.close()
    cur.close()
    
    if update_user is None:
        return jsonify({'message': 'User Not Found'}, 404)

    return jsonify(update_user)


@app.get('/api/users/<id>')
def get_user(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM computadora_on WHERE id = %s', (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User Not Found'}), 404

    print(user)

    return jsonify(user)

@app.get('/')
def home():
    return send_file('static/index.html')
    

if __name__ == '__main__':
    app.run(debug=True)