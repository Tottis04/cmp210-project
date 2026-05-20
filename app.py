from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secretkey"



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['user'] = username
            session['role'] = "admin"
            return redirect('/admin/dashboard')

        elif username == "user" and password == "user123":
            session['user'] = username
            session['role'] = "user"
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


if __name__ == '__main__':
    app.run(debug=True)
