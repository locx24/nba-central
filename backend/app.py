from flask import Flask, render_template
from nba_api.live.nba.endpoints import scoreboard

app = Flask(__name__)

@app.route("/")

def main():
    
    return render_template("index.html")

if __name__ == "__main__":
    
    app.run(debug=True)
    