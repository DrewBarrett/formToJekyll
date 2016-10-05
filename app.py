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
        return "correct usage" + g.get_user()

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, 5000)
