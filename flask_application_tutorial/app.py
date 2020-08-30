from flask import (
    Flask,
    flash,
    g,
    render_template,
    redirect,
    request,
    url_for,
    session,
    logging,
)
from functools import wraps
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3
from data import articles

app = Flask(__name__)

DATABASE = "userdata.db"
Articles = articles()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles")
def articles():
    return render_template("articles.html", articles=Articles)


@app.route("/article/<string:id>/")
def article(id):
    return render_template("article.html", id=id)


class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=50)])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords do not match"),
        ],
    )
    confirm = PasswordField("Confirm Password")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # connects to DB
        con = get_db()

        # Successful, con.commit() is called automatically afterwards
        with con:
            con.execute(
                "INSERT INTO users(name, email, username, password) VALUES(:name, :email, :username, :password)",
                (name, email, username, password),
            )

        # close connection.
        close_connection("exception")

        # flash message.
        flash("You are now registered and can log in", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get form fields
        username = request.form["username"]
        password_candidate = request.form["password"]

        # connect to DB
        conn = get_db()

        # return db row instead of tuples
        conn.row_factory = sqlite3.Row

        # create a db cursor
        cur = conn.cursor()

        try:
            # get user by username
            cur.execute("SELECT * FROM users WHERE username = :username", [username])

            # get the stored hash
            result = cur.fetchone()
            password = result["password"]

            # close connection
            conn.close()

            # compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # user exists in DB and password verified - OK.
                session["logged_in"] = True
                session["username"] = username

                flash("You are nou logged in", "success")
                return redirect(url_for("dashboard"))
            else:
                # user exists in DB but password do not match.
                flash("Invalid login", "danger")
                return render_template("login.html")
        except TypeError:
            flash("User not found", "danger")
            return render_template("login.html")

    return render_template("login.html")


# Checked if user loged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for("login"))

    return wrap


# logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out", "info")
    return redirect(url_for("login"))


# dashboard
@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)
