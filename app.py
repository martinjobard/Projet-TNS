from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template
app = Flask(__name__)

file_loader = FileSystemLoader("./template")

env = Environment(loader = file_loader)

template = env.get_template("test.html")

html = template.render(h1="Tableau de bord",
                       title="Telecom Nancy Service") #Nom du site et contenu principal

@app.route('/')
def hello_world():
    return 'Hello, World!'


print(html)