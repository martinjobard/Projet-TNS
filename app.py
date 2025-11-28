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
    return render_template('Accueil.html', titre=titre_site)

@app.route('/Clients')
def Clients():
    titre_site = "Site interne TNS"
    return render_template('Clients.html', titre=titre_site)

@app.route('/Projets')
def Projets():
    titre_site = "Site interne TNS"
    return render_template('Projets.html', titre=titre_site)

@app.route('/Intervenants')
def Intervenants():
    titre_site = "Site interne TNS"
    return render_template('Intervenants.html', titre=titre_site)

@app.route('/Import-Export')
def Import_Export():
    titre_site = "Site interne TNS"
    return render_template('Import_Export.html', titre=titre_site)

@app.route('/Wiki-Docs')
def Wiki_Docs():
    titre_site = "Site interne TNS"
    return render_template('Wiki_Docs.html', titre=titre_site)

@app.route('/tinder_like')
def tinder_like():
    titre_site = "Site interne TNS"
    return render_template('tinder_like.html', titre=titre_site)

@app.route('/Stats')
def Stats():
    titre_site = "Site interne TNS"
    return render_template('Stats.html', titre=titre_site)

@app.route('/Missions_réalisées')
def Missions_réalisées():
    titre_site = "Site interne TNS"
    return render_template('Missions_réalisées.html', titre=titre_site)

@app.route('/Partenaires')
def Partenaires():
    titre_site = "Site interne TNS"
    return render_template('Partenaires.html', titre=titre_site)

@app.route('/Contact')
def Contact():
    titre_site = "Site interne TNS"
    return render_template('Contact.html', titre=titre_site)

if __name__ == '__main__':
    app.run(debug=True)

