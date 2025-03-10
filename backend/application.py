from flask import Flask, render_template
from nba_api.live.nba.endpoints import scoreboard
import csv

# Initialize the Flask application
app = Flask(__name__)

# Define the main route for displaying the NBA scoreboard
@app.route("/")
def main():
    
    # Fetch the current day's NBA scoreboard data
    games = scoreboard.ScoreBoard().get_dict()
    
    # Initialize an empty list to store processed game data
    gamesData = []
    
    # Extract the list of games from the scoreboard data
    gamesList = games["scoreboard"]["games"]
    
    # Loop through each game and extract relevant details
    for game in gamesList:
        
        # Get the current status of the game (e.g., Final, In Progress)
        gameStatusText = game["gameStatusText"]
        
        # Get the home and away team names
        homeTeam = game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName']
        awayTeam = game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName']
        
        # Get the current score for each team
        homeScore = game['homeTeam']['score']
        awayScore = game['awayTeam']['score']
        
        # Append the extracted game data to the list
        gamesData.append({
            "gameStatusText": gameStatusText,
            "homeTeam": homeTeam,
            "awayTeam": awayTeam,
            "homeScore": homeScore,
            "awayScore": awayScore
        })
    
    # Render the index.html template with the game data
    return render_template("index.html", games=gamesData)

# Define the route for viewing NBA MVP data
@app.route("/mvp")
def mvp():
    
    # Open and read the CSV file containing MVP data
    with open("importedData.csv") as csvToRead:
        
        mvpCSV = csv.reader(csvToRead)
        mvpCSV = list(mvpCSV)  # Convert CSV data into a list

    # Extract unique seasons from the CSV data for dropdown selection
    seasons = sorted(set(row[0] for row in mvpCSV[1:]), reverse=True)

    # Initialize an empty list to store MVP player stats
    extractedData = []
    
    # Loop through the CSV data to extract MVP stats
    for row in mvpCSV[1:]:  
        extractedData.append({
            "Season": row[0],  # NBA season
            "Player Name": row[2],  # MVP player name
            "Points": row[8],  # Points per game
            "Assists": row[10],  # Assists per game
            "Total Rebounds": row[9]  # Rebounds per game
        })
    
    # Render the mvp.html template with the extracted data
    return render_template(
        "mvp.html", 
        seasons=seasons,
        extractedData=extractedData,
    )

# Run the Flask application in debug mode if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)