import csv

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
        
        # Add extracted data to the list
        extractedData.append({
            "Season": season,
            "Player Name": player,
            "Points": pts,
            "Assists": ast,
            "Total Rebouds": trb
        })
    
    # Print the extracted data (for testing purposes)
    for data in extractedData:
        print(data)
  
if __name__ == '__main__':
    main()
