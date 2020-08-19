from flask import Flask, render_template

app = Flask(__name__)

# render_template priveste in folderul templates.
# home.html extends layout.html, astfel foloseste acelasi format al paginii
# ori de cate ori este nevoie.


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
