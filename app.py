"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
import datetime
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
        #s = ""
        #for repo in g.get_user().get_repos():
        #    s+= repo.name + " "
        #s += g.get_user().get_repo("memeplatter.github.io").name
        #for repo in g.get_organization(os.environ.get("GIT_ORG")).get_repos():
        #    s += repo.name + " "
        #s += g.get_organization(os.environ.get("GIT_ORG")).get_repo(os.environ.get("GIT_REPO")).name
        repo = None
        if os.environ.get("GIT_ORG") == None:
            #there is no organization configured
            repo = g.get_user().get_repo(os.environ.get("GIT_REPO"))
        else:
            # there is a organization configured
            repo = g.get_organization(os.environ.get("GIT_ORG")).get_repo(os.environ.get("GIT_REPO"))
        honeypot = request.form["email"]
        
        if len(honeypot) > 0:
            return "eh"
        from_name = request.form['name']
        subject = request.form['subject']
        message = request.form['message']
        createPost(repo, from_name, subject, message)
        return "correct usage " + repo.name
    
def createPost(repo, from_name, subject, message):
    date = datetime.date.isoformat(datetime.date.today())
    path = "/_posts/" + datetime.date.isoformat(datetime.date.today()) + "-" + subject.lower() + ".md"
    commit_message = "Jekyll post by formToJekyll: " + subject
    content = ""
    with open("template.md","r") as myFile:
        content = myFile.read()
    content.replace("{date}", date)
    repo.create_file(path, commit_message, content)
    return

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5000)
