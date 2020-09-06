from flask import Blueprint, render_template, flash
from flask_application_tutorial.auth import get_db

bp = Blueprint("articles", __name__, url_prefix="/articles")


@bp.route("/articles")
def articles():
    # open connection
    con = get_db()

    # return articles
    articles = con.execute("SELECT * FROM articles").fetchall()

    if not articles:
        flash("No articles found", "danger")
        return render_template("articles/articles.html")
    else:
        return render_template("articles/articles.html", articles=articles)


@bp.route("/article/<string:id>/")
def article(id):
    # open connection
    con = get_db()

    # return articles
    article = con.execute("SELECT * FROM articles WHERE id = :id", [id]).fetchone()
    return render_template("articles/article.html", article=article)
