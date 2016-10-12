"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
from flask import Flask
from flask import request
from github import Github
app = Flask(__name__)
g = Github(os.environ.get("GIT_TOKEN"))
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/', methods=["GET", "POST"])
def hello():
    """Renders a sample page."""
    if request.method == "GET":
        return "incorrect usage"
    else:
        s = ""
        for repo in g.get_user().get_repos():
            s+= repo.name + " "
        #s += g.get_user().get_repo("memeplatter.github.io").name
        for repo in g.get_organization(os.environ.get("GIT_ORG")).get_repos():
            s += repo.name + " "
        s += g.get_organization(os.environ.get("GIT_ORG")).get_repo(os.environ.get("GIT_REPO")).name
        return "correct usage " + s
    

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5000)
