# RUn using flask run in the terminal
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from Flask_dojo.engine import Engine

# from wtforms import Form


app = Flask(__name__)

app.config["SECRET_KEY"] = "465d365ce365e8e1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


# Build database
class TextInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    input_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"TextInput('{self.id}', '{self.date}', '{self.input_text}')"


# Dummy input
text_input = [{"input": "adidas sport shoes"}]


# Declare routes of the application
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        input_ = request.form["nm"]
        return redirect(url_for("engine", input=input_))
    else:
        return render_template("home.html")


@app.route("/results", methods=["GET"])
def engine():
    user_input = request.args.get("input")
    results = Engine().text_classification(input_text=user_input, return_prob=True)
    return render_template("results.html", results=results, title="Results")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == "__main__":
    app.run(debug=True)
