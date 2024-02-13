"""Module initilizing application"""

from flask import Flask, request, render_template, send_file
from ai import text_wrapper, logo_wrapper
from slides import make_presentation
from io import BytesIO
from pptx import Presentation

app = Flask(__name__,  instance_relative_config = True)
app.config.from_pyfile("config.py")

@app.route("/", methods =["POST", "GET"])
def create():
    """Function rendering index"""
    if request.method == "POST":
        product_description = request.form["product_description"]
        brand = request.form["brand"]
        text = text_wrapper(product_description, brand, app.config["OPENAI_SECRET_KEY"])
        logo_url = logo_wrapper(text["name"], product_description, brand,
                                app.config["OPENAI_SECRET_KEY"])
        deck = BytesIO()
        prs = make_presentation(text, logo_url)
        prs.save(deck)
        deck.seek(0)
        return send_file(deck, download_name="pitch.pptx", as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
