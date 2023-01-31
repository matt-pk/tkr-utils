from flask import Flask
import name_generator

app = Flask(__name__)


@app.route("/")
def names():
    generated_names = name_generator.generate_name_list()
    return generated_names
