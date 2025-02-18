const express = require("express");
const cors = require("cors");

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// Sample MVP data (replace this with real data from your database or source)
const mvpData = [
  { season: "2021-2022", player: "Giannis Antetokounmpo", points: 29, assists: 5, rebounds: 11 },
  { season: "2020-2021", player: "Nikola Jokic", points: 26, assists: 8, rebounds: 11 },
  { season: "2019-2020", player: "LeBron James", points: 25, assists: 8, rebounds: 8 },
];

// Route to get MVP data
app.get("/mvp", (req, res) => {
  res.json(mvpData);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
