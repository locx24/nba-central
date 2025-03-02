from flask import Flask, render_template
from nba_api.live.nba.endpoints import scoreboard
import csv

app = Flask(__name__)


# main screen for viewing the current day scoreboard
@app.route("/")

def main():
    

    games = scoreboard.ScoreBoard().get_dict()
    
    gamesData= []
    
    gamesList = games["scoreboard"]["games"]
    
    for game in gamesList:
        
        gameStatusText = game["gameStatusText"]
        
        homeTeam = game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName']
        awayTeam = game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName']
        
        homeScore = game['homeTeam']['score']
        awayScore = game['awayTeam']['score']
                
        gamesData.append({
            "gameStatusText": gameStatusText,
            "homeTeam": homeTeam,
            "awayTeam": awayTeam,
            "homeScore": homeScore,
            "awayScore": awayScore
            })
    
    # return live scoreboard    
    return render_template("index.html", games = gamesData)

# screen for getting nba mvp data 
@app.route("/mvp")

def mvp():
    
    # open CSV file for MVP data
    with open("importedData.csv") as csvToRead:
        mvpCSV = csv.reader(csvToRead)
        mvpCSV = list(mvpCSV)  

    # extract unique seasons for the dropdown
    seasons = sorted(set(row[0] for row in mvpCSV[1:]), reverse=True)

    # extract player stats
    extractedData = []
    
    for row in mvpCSV[1:]:  
        extractedData.append({
            "Season": row[0],
            "Player Name": row[2],
            "Points": row[8],
            "Assists": row[10],
            "Total Rebounds": row[9]
        })
        
    # return mvp data
    return render_template("mvp.html", seasons = seasons,extractedData = extractedData)

if __name__ == "__main__":
    
    app.run(debug=True)
    