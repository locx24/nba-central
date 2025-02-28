import csv
import pandas as pd
from nba_api.live.nba.endpoints import scoreboard

def main():
    
    # open csv file that contains the mvp data
    with open("nba_data.csv") as csvToRead:
        
        # store data in a list 
        mvpCSV = csv.reader(csvToRead)    
        mvpCSV = list(mvpCSV)  
        
    # create a list to store the desired columns 
    extractedData = []
    
    # loop over the rows and extract the desired columns
    # skip header row
    for row in mvpCSV[1:]:  
        season = row[0]
        player = row[2]
        pts = row[8]
        ast = row[10]
        trb = row[9]
        
        # add extracted data to the list
        extractedData.append({
            "Season": season,
            "Player Name": player,
            "Points": pts,
            "Assists": ast,
            "Total Rebouds": trb
        })
    
    # print the extracted data
    #for data in extractedData:
     #   print(data)
     
    games = scoreboard.ScoreBoard()
    
    data = games.get_dict()
    
    gameList = data["scoreboard"]["games"]
    
    for game in gameList:
        
        
        homeTeam = game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName']
        awayTeam = game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName']
        
        homeScore = game['homeTeam']['score']
        awayScore = game['awayTeam']['score']
        
        print(f"{awayTeam} {awayScore} - {homeTeam} {homeScore}\n") 
        
        
if __name__ == '__main__':
    main()