from flask import Flask, render_template, request, redirect, session, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='statics')
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

            if user[3] == 'admin':
                return redirect('/admin/dashboard')

            else:
                return redirect('/user/dashboard')

        else:
            return "Invalid credentials"

    return render_template('login.html')


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

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM players")
    total_players = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM teams")
    total_teams = cur.fetchone()[0]

    try:
        cur.execute("SELECT COUNT(*) FROM matches")
        total_matches = cur.fetchone()[0]
    except Exception:
        total_matches = 0

    cur.close()

    return render_template("user/dashboard.html",
                           total_players=total_players,
                           total_teams=total_teams,
                           total_matches=total_matches)


@app.route('/admin/dashboard')
def admin_dashboard():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return "Access denied"

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM players")
    total_players = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM teams")
    total_teams = cur.fetchone()[0]

    try:
        cur.execute("SELECT COUNT(*) FROM matches")
        total_matches = cur.fetchone()[0]
    except Exception:
        total_matches = 0

    cur.close()

    return render_template("admin/dashboard.html",
                           total_players=total_players,
                           total_teams=total_teams,
                           total_matches=total_matches)


@app.route('/players')
def players():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM players")

    players = cur.fetchall()

    cur.close()

    return render_template("admin/players.html", players=players)

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

    return render_template('admin/add_player.html')


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

    return render_template('admin/edit_player.html', player=player)



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


@app.route('/teams')
def teams():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM teams")
    teams = cur.fetchall()
    cur.close()
    return render_template("admin/teams.html", teams=teams)


@app.route('/add-team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name         = request.form['name']
        coach        = request.form['coach']
        stadium      = request.form['stadium']
        founded_year = request.form['founded_year']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO teams(name, coach, stadium, founded_year) VALUES(%s, %s, %s, %s)",
            (name, coach, stadium, founded_year)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/teams')
    return render_template('admin/add_team.html')


@app.route('/delete-team/<int:id>')
def delete_team(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM teams WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/teams')


@app.route('/edit-team/<int:id>', methods=['GET', 'POST'])
def edit_team(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name         = request.form['name']
        coach        = request.form['coach']
        stadium      = request.form['stadium']
        founded_year = request.form['founded_year']
        cur.execute(
            "UPDATE teams SET name=%s, coach=%s, stadium=%s, founded_year=%s WHERE id=%s",
            (name, coach, stadium, founded_year, id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/teams')
    cur.execute("SELECT * FROM teams WHERE id = %s", (id,))
    team = cur.fetchone()
    cur.close()
    return render_template('admin/edit_team.html', team=team)


@app.route('/matches')
def matches():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matches ORDER BY match_date DESC")
    matches = cur.fetchall()
    cur.close()
    return render_template('admin/matches.html', matches=matches)


@app.route('/add-match', methods=['GET', 'POST'])
def add_match():
    if request.method == 'POST':
        home_team  = request.form['home_team']
        away_team  = request.form['away_team']
        match_date = request.form['match_date']
        stadium    = request.form['stadium']
        home_score = request.form['home_score']
        away_score = request.form['away_score']
        status     = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO matches(home_team, away_team, match_date, stadium, home_score, away_score, status) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (home_team, away_team, match_date, stadium, home_score, away_score, status)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/matches')
    return render_template('admin/add_match.html')


@app.route('/delete-match/<int:id>')
def delete_match(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM matches WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/matches')


@app.route('/edit-match/<int:id>', methods=['GET', 'POST'])
def edit_match(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        home_team  = request.form['home_team']
        away_team  = request.form['away_team']
        match_date = request.form['match_date']
        stadium    = request.form['stadium']
        home_score = request.form['home_score']
        away_score = request.form['away_score']
        status     = request.form['status']
        cur.execute(
            "UPDATE matches SET home_team=%s, away_team=%s, match_date=%s, stadium=%s, home_score=%s, away_score=%s, status=%s WHERE id=%s",
            (home_team, away_team, match_date, stadium, home_score, away_score, status, id)
        )
        mysql.connection.commit()
        cur.close()
        return redirect('/matches')
    cur.execute("SELECT * FROM matches WHERE id = %s", (id,))
    match = cur.fetchone()
    cur.close()
    return render_template('admin/edit_match.html', match=match)


@app.route('/statistics')
def statistics():
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM players")
    total_players = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM teams")
    total_teams = cur.fetchone()[0]

    cur.execute("SELECT ROUND(AVG(age), 1) FROM players")
    avg_age = cur.fetchone()[0] or 0

    try:
        cur.execute("SELECT COUNT(*) FROM matches")
        total_matches = cur.fetchone()[0]
    except Exception:
        total_matches = 0

    cur.execute("SELECT name, team, position, age FROM players ORDER BY age DESC")
    players = cur.fetchall()

    try:
        cur.execute("SELECT home_team, away_team, match_date, stadium FROM matches ORDER BY match_date DESC LIMIT 10")
        matches = cur.fetchall()
    except Exception:
        matches = []

    cur.close()

    return render_template('admin/statistics.html',
                           total_players=total_players,
                           total_teams=total_teams,
                           total_matches=total_matches,
                           avg_age=avg_age,
                           players=players,
                           matches=matches)


@app.route('/api-info')
def api_info():
    return render_template('admin/api_info.html')


@app.route('/user/players')
def user_players():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'user':
        return "Access denied"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM players")
    players = cur.fetchall()
    cur.close()

    return render_template('user/players.html', players=players)


@app.route('/user/teams')
def user_teams():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'user':
        return "Access denied"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM teams")
    teams = cur.fetchall()
    cur.close()

    return render_template('user/teams.html', teams=teams)


@app.route('/user/statistics')
def user_statistics():

    if 'user' not in session:
        return redirect('/login')

    if session['role'] != 'user':
        return "Access denied"

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM players")
    total_players = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM teams")
    total_teams = cur.fetchone()[0]

    cur.execute("SELECT ROUND(AVG(age), 1) FROM players")
    avg_age = cur.fetchone()[0] or 0

    try:
        cur.execute("SELECT COUNT(*) FROM matches")
        total_matches = cur.fetchone()[0]
    except Exception:
        total_matches = 0

    cur.execute("SELECT name, team, position, age FROM players ORDER BY age DESC")
    players = cur.fetchall()

    try:
        cur.execute("SELECT home_team, away_team, match_date, stadium FROM matches ORDER BY match_date DESC LIMIT 10")
        matches = cur.fetchall()
    except Exception:
        matches = []

    cur.close()

    return render_template('user/statistics.html',
                           total_players=total_players,
                           total_teams=total_teams,
                           total_matches=total_matches,
                           avg_age=avg_age,
                           players=players,
                           matches=matches)


if __name__ == '__main__':
    app.run(debug=True)