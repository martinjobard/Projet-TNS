from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("./template")

env = Environment(loader = file_loader)

template = env.get_template("test.html")

html = template.render(h1="Tableau de bord",
                       title="Telecom Nancy Service") #Nom du site et contenu principal

print(html)