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
from data import articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3

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
        # create cursor
        cur = get_db().cursor()
        cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES(:name, :email, :username, :password)",
            (name, email, username, password),
        )
        flash("You are now registered and log in", "succes")
        redirect(url_for("index"))

    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)
