from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'sports_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            session['user'] = user[1]
            session['role'] = user[3]

            if user[3] == "admin":
                return redirect('/admin/dashboard')

            elif user[3] == "user":
                return redirect('/user/dashboard')

        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


@app.route('/user/dashboard')
def user_dashboard():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'user':
        return "Access denied"

    return render_template("user/dashboard.html")


@app.route('/admin/dashboard')
def admin_dashboard():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return "Access denied"

    return render_template("admin/dashboard.html")


@app.route('/players')
def players():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM players")

    players = cur.fetchall()

    cur.close()

    return render_template("players.html", players=players)

@app.route('/add-player', methods=['GET', 'POST'])
def add_player():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        team = request.form['team']
        position = request.form['position']

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO players(name, age, team, position) VALUES(%s, %s, %s, %s)",
            (name, age, team, position)
        )

        mysql.connection.commit()

        cur.close()

        return redirect('/players')

    return render_template('add_player.html')


@app.route('/delete-player/<int:id>')
def delete_player(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM players WHERE id = %s", (id,))

    mysql.connection.commit()

    cur.close()

    return redirect('/players')


@app.route('/edit-player/<int:id>', methods=['GET', 'POST'])
def edit_player(id):

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        team = request.form['team']
        position = request.form['position']

        cur.execute(
            "UPDATE players SET name=%s, age=%s, team=%s, position=%s WHERE id=%s",
            (name, age, team, position, id)
        )

        mysql.connection.commit()

        cur.close()

        return redirect('/players')

    cur.execute("SELECT * FROM players WHERE id = %s", (id,))

    player = cur.fetchone()

    cur.close()

    return render_template('edit_player.html', player=player)



@app.route('/api/players')
def api_players():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM players")

    players = cur.fetchall()

    cur.close()

    data = []

    for player in players:

        player_data = {
            "id": player[0],
            "name": player[1],
            "age": player[2],
            "team": player[3],
            "position": player[4]
        }

        data.append(player_data)

    return jsonify(data)

@app.route('/api/users')
def api_users():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    cur.close()

    data = []

    for user in users:

        user_data = {
            "id": user[0],
            "username": user[1],
            "role": user[3]
        }

        data.append(user_data)

    return jsonify(data)

@app.route('/api/reports/player-count')
def player_count():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM players")

    total = cur.fetchone()

    cur.close()

    return jsonify({
        "total_players": total[0]
    })


@app.route('/api/oldest-player')
def oldest_player():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM players ORDER BY age DESC LIMIT 1")

    player = cur.fetchone()

    cur.close()

    data = {
        "id": player[0],
        "name": player[1],
        "age": player[2],
        "team": player[3],
        "position": player[4]
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)