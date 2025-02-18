import { useState, useEffect } from "react";

function App() {
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState("");
  const [mvp, setMvp] = useState(null);

  useEffect(() => {
    // Fetch data from backend
    fetch("http://localhost:3001/mvp")
      .then((res) => res.json())
      .then((data) => {
        // Set unique seasons
        setSeasons([...new Set(data.map((entry) => entry.season))]);
      });
  }, []);

  const handleSeasonChange = (event) => {
    setSelectedSeason(event.target.value);
    
    // Fetch MVP data based on the selected season from the correct backend URL
    fetch(`http://localhost:3001/mvp`)
      .then((res) => res.json())
      .then((data) => {
        // Find the season data based on the selected season
        const seasonData = data.find((entry) => entry.season === event.target.value);
        setMvp(seasonData);
      });
  };

  return (
    <div>
      <h1>NBA MVP Data</h1>
      <label>Select a Season:</label>
      <select value={selectedSeason} onChange={handleSeasonChange}>
        <option value="">-- Choose a Season --</option>
        {seasons.map((season, index) => (
          <option key={index} value={season}>{season}</option>
        ))}
      </select>

      {mvp && (
        <div>
          <h2>{mvp.player}</h2>
          <p>Points: {mvp.points}</p>
          <p>Assists: {mvp.assists}</p>
          <p>Rebounds: {mvp.rebounds}</p>
        </div>
      )}
    </div>
  );
}

export default App;
