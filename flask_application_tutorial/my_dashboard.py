from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_application_tutorial.db import get_db
from flask_application_tutorial.forms import ArticleForm
from flask_application_tutorial.auth import is_logged_in

bp = Blueprint("my_dashboard", __name__, url_prefix="/my_dashboard")


# dashboard
@bp.route("/dashboard")
@is_logged_in
def dashboard():
    username = session["username"]
    # open connection
    con = get_db()

    # return articles
    articles = con.execute(
        "SELECT * FROM articles WHERE author=:username", [username]
    ).fetchall()

    if not articles:
        flash("No articles found", "danger")
        return render_template("my_dashboard/dashboard.html")
    else:
        return render_template("my_dashboard/dashboard.html", articles=articles)


# add articles
@bp.route("/add_article", methods=["GET", "POST"])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data
        username = session["username"]

        # open connection to DB
        con = get_db()
        with con:
            con.execute(
                "INSERT INTO articles(title, body, author) VALUES(:title, :body, :author)",
                (title, body, username),
            )
        # flash message
        flash("Article created", "success")

        return redirect(url_for("my_dashboard.dashboard"))
    return render_template("my_dashboard/add_article.html", form=form)


# edit articles
@bp.route("/edit_article/<string:id>", methods=["GET", "POST"])
@is_logged_in
def edit_article(id):
    # open connection
    con = get_db()

    # return article to edit
    article = con.execute("SELECT * FROM articles WHERE id = :id", [id]).fetchone()

    # get article form
    form = ArticleForm(request.form)

    # populate article form fields
    form.title.data = article["title"]
    form.body.data = article["body"]

    if request.method == "POST" and form.validate():
        title = request.form["title"]
        body = request.form["body"]

        # update article fields
        with con:
            con.execute(
                "UPDATE articles SET title=:title, body=:body WHERE id=:id",
                [title, body, id],
            )

        # flash message
        flash("Article updated", "success")
        return redirect(url_for("my_dashboard.dashboard"))
    return render_template("my_dashboard/edit_article.html", form=form)


# delete article
@bp.route("/delete_article/<string:id>", methods=["POST"])
@is_logged_in
def delete_article(id):
    # open connection
    con = get_db()

    with con:
        # return article to delete
        con.execute("DELETE FROM articles WHERE id=:id", [id])

    flash("Article deleted", "success")
    return redirect(url_for("my_dashboard.dashboard"))


def articles_count():
    username = session["username"]
    con = get_db
    with con:
        con.execute(
            "SELECT * FROM articles WHERE author=:username", [username]
        ).rowcount
        article_count = con.fetchall()
    return article_count
