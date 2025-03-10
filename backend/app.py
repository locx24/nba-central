from flask import Flask, render_template
from nba_api.live.nba.endpoints import scoreboard
import csv
import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key for Highlightly from environment variables
HIGHLIGHTLY_API_KEY = os.getenv("HIGHLIGHTLY_API_KEY")

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
    
    # API call to get highlight video for the most recent MVP
    highlightURL = f"https://api.highlightly.net/highlights/player/Stephen%20Curry"
    headers = {"Authorization": f"Bearer {HIGHLIGHTLY_API_KEY}"}
    
    try:
        # Send a GET request to the highlight API
        response = requests.get(highlightURL, headers=headers)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()  
        
        # Parse the JSON response
        highlightData = response.json()
        
        # Extract the highlight video URL if available
        highlightVideoURL = highlightData.get("video_url", "")
        
    except requests.exceptions.RequestException as e:
        # Print an error message if the API request fails
        print(f"Error fetching highlight: {e}")
        
        # Set an empty string as the highlight video URL in case of failure
        highlightVideoURL = ""
    
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
        highlightVideoURL=highlightVideoURL
    )

# Run the Flask application in debug mode if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=5001)