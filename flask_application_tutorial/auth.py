from functools import wraps
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_application_tutorial.db import get_db
from flask_application_tutorial.forms import RegisterForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


# register route
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(str(form.password.data))

        # connects to DB
        con = get_db()

        # Successful, con.commit() is called automatically afterwards
        try:

            with con:
                con.execute(
                    "INSERT INTO users(name, email, username, password) VALUES(:name, :email, :username, :password)",
                    (name, email, username, password),
                )
            # flash message.
            flash("You are now registered and can log in", "success")

            return redirect(url_for("auth.login"))

        except Exception:
            flash("User already in database", "danger")

    return render_template("auth/register.html", form=form)


# login route
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get form fields
        username = request.form["username"]
        password = request.form["password"]
        # connect to DB
        con = get_db()
        # search for user in the data base
        user = con.execute(
            "SELECT * FROM users WHERE username = :username", [username]
        ).fetchone()

        if user is None:
            # user not found in data base
            flash("User not found", "danger")
            return render_template("auth/login.html")
        elif not check_password_hash(user["password"], password):
            # user exists in DB but password do not match.
            flash("Invalid login", "danger")
            return render_template("auth/login.html")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("You are now logged in", "success")
            return redirect(url_for("my_dashboard.dashboard"))
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_name = session.get("username")

    if user_name is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute("SELECT * FROM users WHERE username = :user_name", [user_name])
            .fetchone()
        )


def is_logged_in(view):
    """Wraps a fuction that checks if a user is logged in.
    """

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for("auth.login"))
        else:
            return view(**kwargs)

    return wrapped_view


# logout route
@bp.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out", "info")
    return redirect(url_for("auth.login"))
