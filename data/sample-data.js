export const storyCards = [
  {
    title: "Set up the tension",
    text: "Barcelona's identity is built on possession, but the first visual should challenge whether that identity still predicts winning, especially away from home.",
  },
  {
    title: "Move from symptom to response",
    text: "Once the audience sees possession can fail, the next question becomes practical: which player profiles can help the team preserve control under pressure?",
  },
  {
    title: "Name the difficult opponents",
    text: "The third view narrows the problem by revealing which opponents suppress Barcelona's attack, creating a bridge from style to matchup strategy.",
  },
  {
    title: "End with context and action",
    text: "The final benchmark visual resolves the story by placing Barcelona among elite clubs and grounding recommendations in comparison rather than opinion.",
  },
];

export const questions = [
  "Does dominating possession really translate into wins?",
  "Which players show the strongest development for the desired style?",
  "Which opponents reduce Barcelona's attacking output the most?",
  "How does Barcelona compare with Europe's top clubs overall?",
];

export const possessionMatches = [
  { opponent: "Real Madrid", venue: "Home", possession: 61, result: "Win", goalsFor: 3, goalsAgainst: 1 },
  { opponent: "Atletico", venue: "Away", possession: 58, result: "Draw", goalsFor: 1, goalsAgainst: 1 },
  { opponent: "Girona", venue: "Away", possession: 65, result: "Loss", goalsFor: 2, goalsAgainst: 4 },
  { opponent: "Sevilla", venue: "Home", possession: 63, result: "Win", goalsFor: 2, goalsAgainst: 0 },
  { opponent: "Valencia", venue: "Away", possession: 54, result: "Win", goalsFor: 2, goalsAgainst: 1 },
  { opponent: "Villarreal", venue: "Away", possession: 67, result: "Loss", goalsFor: 1, goalsAgainst: 2 },
  { opponent: "Sociedad", venue: "Home", possession: 56, result: "Draw", goalsFor: 0, goalsAgainst: 0 },
  { opponent: "Bilbao", venue: "Away", possession: 59, result: "Loss", goalsFor: 0, goalsAgainst: 1 },
  { opponent: "Betis", venue: "Home", possession: 62, result: "Win", goalsFor: 4, goalsAgainst: 2 },
  { opponent: "Osasuna", venue: "Away", possession: 60, result: "Win", goalsFor: 2, goalsAgainst: 0 },
  { opponent: "Celta", venue: "Home", possession: 64, result: "Win", goalsFor: 3, goalsAgainst: 0 },
  { opponent: "Mallorca", venue: "Away", possession: 57, result: "Draw", goalsFor: 1, goalsAgainst: 1 },
];

export const scoutingPlayers = [
  {
    player: "Pedri",
    values: [
      { season: "2020", score: 70 },
      { season: "2021", score: 76 },
      { season: "2022", score: 82 },
      { season: "2023", score: 86 },
    ],
  },
  {
    player: "Gavi",
    values: [
      { season: "2020", score: 58 },
      { season: "2021", score: 69 },
      { season: "2022", score: 77 },
      { season: "2023", score: 84 },
    ],
  },
  {
    player: "Fermin",
    values: [
      { season: "2020", score: 44 },
      { season: "2021", score: 55 },
      { season: "2022", score: 66 },
      { season: "2023", score: 76 },
    ],
  },
  {
    player: "De Jong",
    values: [
      { season: "2020", score: 75 },
      { season: "2021", score: 78 },
      { season: "2022", score: 80 },
      { season: "2023", score: 81 },
    ],
  },
];

export const kryptoniteMatrix = [
  { opponent: "Girona", season: "2021", goals: 1.1 },
  { opponent: "Girona", season: "2022", goals: 0.9 },
  { opponent: "Girona", season: "2023", goals: 1.0 },
  { opponent: "Athletic", season: "2021", goals: 0.8 },
  { opponent: "Athletic", season: "2022", goals: 1.0 },
  { opponent: "Athletic", season: "2023", goals: 0.7 },
  { opponent: "Atletico", season: "2021", goals: 1.4 },
  { opponent: "Atletico", season: "2022", goals: 1.2 },
  { opponent: "Atletico", season: "2023", goals: 1.1 },
  { opponent: "Madrid", season: "2021", goals: 2.0 },
  { opponent: "Madrid", season: "2022", goals: 1.8 },
  { opponent: "Madrid", season: "2023", goals: 1.7 },
  { opponent: "PSG", season: "2021", goals: 1.3 },
  { opponent: "PSG", season: "2022", goals: 1.2 },
  { opponent: "PSG", season: "2023", goals: 1.5 },
];

export const benchmarkClubs = [
  { club: "Barcelona", possession: 61, goalsPerGame: 2.1, pointsPerGame: 2.2 },
  { club: "Real Madrid", possession: 57, goalsPerGame: 2.3, pointsPerGame: 2.4 },
  { club: "Manchester City", possession: 64, goalsPerGame: 2.5, pointsPerGame: 2.5 },
  { club: "Bayern", possession: 60, goalsPerGame: 2.4, pointsPerGame: 2.3 },
  { club: "PSG", possession: 59, goalsPerGame: 2.2, pointsPerGame: 2.1 },
  { club: "Arsenal", possession: 58, goalsPerGame: 2.0, pointsPerGame: 2.2 },
];

export const reportNotes = [
  {
    title: "Explain the narrative order",
    text: "In the report, justify the sequence of visuals as a storyline: diagnosis, response, vulnerable opponents, and benchmarked conclusion.",
  },
  {
    title: "State what changed after feedback",
    text: "Mention the direct-label replacement in the scouting view, the corrected heatmap colour scale, and the stronger introduction and conclusion panels.",
  },
  {
    title: "Connect design to theory",
    text: "Tie each choice back to design principles such as position on common scale, pre-attentive contrast, direct labelling, and reduced cognitive load.",
  },
  {
    title: "Leave room for evidence",
    text: "Add screenshots, final metric values, repository link, and video link once the real data and finished UI are ready.",
  },
];
