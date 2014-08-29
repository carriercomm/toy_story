import os
from flask import Flask, render_template

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG=True,
)


# controllers
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/leaderboard/<org>/<repo>")
def leaderboard(org, repo):
    repo = {'org': org, 'repo': repo}
    return render_template('leaderboard.html', repo=repo)


@app.route("/user/<org>/<repo>/<username>")
def user_profile(org, repo, username):
    user = {'org': org, 'repo': repo, 'username': username}
    return render_template('user.html', user=user)

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
