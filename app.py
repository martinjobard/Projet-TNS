from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template
app = Flask(__name__)
"""
file_loader = FileSystemLoader("./template")

env = Environment(loader = file_loader)

template = env.get_template("test.html")

html = template.render(h1="Tableau de bord",
                       title="Telecom Nancy Service") #Nom du site et contenu principal
"""
@app.route('/')
def Accueil():
    titre_site = "Site interne TNS"
    return render_template('Accueil.html',titre = titre_site)

@app.route('/Clients')
def Clients():
    return 'Hello, World!'

@app.route('/Projets')
def Projets():
    return 'Hello, World!'

@app.route('/Intervenants')
def Intervenants():
    return 'Hello, World!'

@app.route('/Import-Export')
def Import_Export():
    return 'Hello, World!'

@app.route('/Wiki-Docs')
def Wiki_Docs():
    return 'Hello, World!'

@app.route('/tinder_like')
def tinder_like():
    return 'Hello, World!'

@app.route('/Stats')
def Stats():
    return 'Hello, World!'

@app.route('/Missions_réalisées')
def Missions_réalisées():
    return 'Hello, World!'

@app.route('/Partenaires')
def Partenaires():
    return 'Hello, World!'

@app.route('/Contact')
def Contact():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

