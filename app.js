import {
  benchmarkClubs,
  kryptoniteMatrix,
  possessionMatches,
  questions,
  reportNotes,
  scoutingPlayers,
  storyCards,
} from "./data/sample-data.js";

const svgNs = "http://www.w3.org/2000/svg";
const tooltip = document.querySelector("#tooltip");

const palette = {
  win: "#2f7d60",
  draw: "#d6a74d",
  loss: "#bb4d4d",
  accent: "#912f40",
  accent2: "#2f5d62",
  warm: "#bf5a33",
  ink: "#1f2a30",
  muted: "#5e6a70",
};

function createSvgNode(tag, attrs = {}) {
  const node = document.createElementNS(svgNs, tag);
  for (const [key, value] of Object.entries(attrs)) {
    node.setAttribute(key, value);
  }
  return node;
}

function clearSvg(svg) {
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
}

function showTooltip(content, event) {
  tooltip.hidden = false;
  tooltip.innerHTML = content;
  tooltip.style.left = `${event.clientX + 18}px`;
  tooltip.style.top = `${event.clientY + 18}px`;
}

function hideTooltip() {
  tooltip.hidden = true;
}

function scaleLinear(value, minValue, maxValue, minPixel, maxPixel) {
  const ratio = (value - minValue) / (maxValue - minValue || 1);
  return minPixel + ratio * (maxPixel - minPixel);
}

function drawText(svg, x, y, text, className, anchor = "start") {
  const node = createSvgNode("text", { x, y, class: className, "text-anchor": anchor });
  node.textContent = text;
  svg.appendChild(node);
}

function mountCards() {
  const storyHost = document.querySelector("#story-cards");
  const reportHost = document.querySelector("#report-cards");
  const questionHost = document.querySelector("#question-strip");

  storyCards.forEach((card, index) => {
    const article = document.createElement("article");
    article.className = "story-card";
    article.innerHTML = `<span class="step">${index + 1}</span><h3>${card.title}</h3><p>${card.text}</p>`;
    storyHost.appendChild(article);
  });

  reportNotes.forEach((card, index) => {
    const article = document.createElement("article");
    article.className = "report-card";
    article.innerHTML = `<span class="step">${index + 1}</span><h3>${card.title}</h3><p>${card.text}</p>`;
    reportHost.appendChild(article);
  });

  questions.forEach((question, index) => {
    const pill = document.createElement("div");
    pill.className = "question-pill";
    pill.innerHTML = `<strong>Q${index + 1}</strong><span>${question}</span>`;
    questionHost.appendChild(pill);
  });
}

function renderPossessionChart(filter = "all") {
  const svg = document.querySelector("#chart-possession");
  const summary = document.querySelector("#possession-summary");
  clearSvg(svg);

  const matches = possessionMatches.filter(
    (match) => filter === "all" || match.venue === filter,
  );

  const width = 740;
  const height = 420;
  const margin = { top: 30, right: 30, bottom: 60, left: 70 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;

  const resultOrder = ["Loss", "Draw", "Win"];
  const colors = { Win: palette.win, Draw: palette.draw, Loss: palette.loss };

  for (const threshold of [45, 50, 55, 60, 65, 70]) {
    const x = scaleLinear(threshold, 45, 70, margin.left, width - margin.right);
    svg.appendChild(createSvgNode("line", { x1: x, y1: margin.top, x2: x, y2: height - margin.bottom, class: "gridline" }));
    drawText(svg, x, height - 34, `${threshold}%`, "label", "middle");
  }

  resultOrder.forEach((result, index) => {
    const y = margin.top + 38 + index * (plotHeight / 3);
    svg.appendChild(createSvgNode("line", { x1: margin.left, y1: y, x2: width - margin.right, y2: y, class: "reference-line" }));
    drawText(svg, margin.left - 16, y + 4, result, "title-label", "end");
  });

  matches.forEach((match, index) => {
    const x = scaleLinear(match.possession, 45, 70, margin.left, width - margin.right);
    const baseY = margin.top + 38 + resultOrder.indexOf(match.result) * (plotHeight / 3);
    const y = baseY + ((index % 5) - 2) * 10;
    const circle = createSvgNode("circle", {
      cx: x,
      cy: y,
      r: 9,
      fill: colors[match.result],
      opacity: 0.9,
    });
    circle.addEventListener("mousemove", (event) => {
      showTooltip(
        `<strong>${match.opponent}</strong><br>${match.venue} match<br>Possession: ${match.possession}%<br>Score: ${match.goalsFor}-${match.goalsAgainst}`,
        event,
      );
    });
    circle.addEventListener("mouseleave", hideTooltip);
    svg.appendChild(circle);
  });

  drawText(svg, width / 2, 20, "Ball possession by match outcome", "title-label", "middle");
  drawText(svg, width / 2, height - 12, "Barcelona possession share", "label", "middle");

  const highPossessionLosses = matches.filter(
    (match) => match.result === "Loss" && match.possession >= 58,
  ).length;

  summary.textContent =
    `${highPossessionLosses} high-possession ${filter === "all" ? "" : filter.toLowerCase() + " "}matches still ended in defeat in the sample data, which creates the narrative tension for the rest of the story.`;
}

function renderPlayerToggles(activePlayers) {
  const host = document.querySelector("#player-toggles");
  host.innerHTML = "";

  scoutingPlayers.forEach((player) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `toggle-chip ${activePlayers.includes(player.player) ? "active" : ""}`;
    button.textContent = player.player;
    button.addEventListener("click", () => {
      const next = activePlayers.includes(player.player)
        ? activePlayers.filter((name) => name !== player.player)
        : [...activePlayers, player.player];
      renderScoutingChart(next.length ? next : [player.player]);
    });
    host.appendChild(button);
  });
}

function renderScoutingChart(activePlayers = scoutingPlayers.map((player) => player.player)) {
  const svg = document.querySelector("#chart-scouting");
  const summary = document.querySelector("#scouting-summary");
  clearSvg(svg);
  renderPlayerToggles(activePlayers);

  const width = 740;
  const height = 420;
  const margin = { top: 36, right: 90, bottom: 60, left: 70 };
  const years = scoutingPlayers[0].values.map((value) => value.season);

  years.forEach((season, index) => {
    const x = scaleLinear(index, 0, years.length - 1, margin.left, width - margin.right);
    svg.appendChild(createSvgNode("line", { x1: x, y1: margin.top, x2: x, y2: height - margin.bottom, class: "gridline" }));
    drawText(svg, x, height - 32, season, "label", "middle");
  });

  [40, 50, 60, 70, 80, 90].forEach((value) => {
    const y = scaleLinear(value, 40, 90, height - margin.bottom, margin.top);
    svg.appendChild(createSvgNode("line", { x1: margin.left, y1: y, x2: width - margin.right, y2: y, class: "gridline" }));
    drawText(svg, margin.left - 12, y + 4, `${value}`, "label", "end");
  });

  const visiblePlayers = scoutingPlayers.filter((player) => activePlayers.includes(player.player));
  const lineColors = ["#912f40", "#2f5d62", "#d97d54", "#4b7f52"];

  visiblePlayers.forEach((player, index) => {
    const points = player.values.map((value, seasonIndex) => {
      const x = scaleLinear(seasonIndex, 0, years.length - 1, margin.left, width - margin.right);
      const y = scaleLinear(value.score, 40, 90, height - margin.bottom, margin.top);
      return { x, y, ...value };
    });

    const pathData = points.map((point, pointIndex) => `${pointIndex === 0 ? "M" : "L"} ${point.x} ${point.y}`).join(" ");
    const color = lineColors[index % lineColors.length];
    svg.appendChild(
      createSvgNode("path", {
        d: pathData,
        fill: "none",
        stroke: color,
        "stroke-width": 3,
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
      }),
    );

    points.forEach((point) => {
      const circle = createSvgNode("circle", { cx: point.x, cy: point.y, r: 5, fill: color });
      circle.addEventListener("mousemove", (event) => {
        showTooltip(
          `<strong>${player.player}</strong><br>Season: ${point.season}<br>Development score: ${point.score}`,
          event,
        );
      });
      circle.addEventListener("mouseleave", hideTooltip);
      svg.appendChild(circle);
    });

    const last = points[points.length - 1];
    drawText(svg, last.x + 10, last.y + 4, player.player, "title-label");
  });

  drawText(svg, width / 2, 20, "Player development for short-passing style", "title-label", "middle");
  drawText(svg, width / 2, height - 12, "Season", "label", "middle");

  const ranking = [...scoutingPlayers]
    .sort((a, b) => b.values.at(-1).score - a.values.at(-1).score)
    .map((player) => `${player.player} (${player.values.at(-1).score})`)
    .join(", ");

  summary.textContent =
    `The chart stays readable because labels sit directly on the lines. Current ranking in the sample data: ${ranking}.`;
}

function renderKryptoniteChart() {
  const svg = document.querySelector("#chart-kryptonite");
  const summary = document.querySelector("#kryptonite-summary");
  clearSvg(svg);

  const width = 740;
  const height = 420;
  const margin = { top: 50, right: 30, bottom: 60, left: 100 };

  const seasons = [...new Set(kryptoniteMatrix.map((d) => d.season))];
  const averages = {};

  kryptoniteMatrix.forEach((cell) => {
    averages[cell.opponent] = averages[cell.opponent] || [];
    averages[cell.opponent].push(cell.goals);
  });

  const opponents = Object.entries(averages)
    .sort((a, b) => a[1].reduce((sum, value) => sum + value, 0) / a[1].length - b[1].reduce((sum, value) => sum + value, 0) / b[1].length)
    .map(([opponent]) => opponent);

  const cellWidth = (width - margin.left - margin.right) / seasons.length;
  const cellHeight = (height - margin.top - margin.bottom) / opponents.length;
  const minGoals = Math.min(...kryptoniteMatrix.map((d) => d.goals));
  const maxGoals = Math.max(...kryptoniteMatrix.map((d) => d.goals));

  const heatColor = (value) => {
    const t = (value - minGoals) / (maxGoals - minGoals || 1);
    const light = 92 - t * 42;
    const sat = 36 + t * 38;
    return `hsl(14 ${sat}% ${light}%)`;
  };

  seasons.forEach((season, columnIndex) => {
    const x = margin.left + columnIndex * cellWidth + cellWidth / 2;
    drawText(svg, x, margin.top - 14, season, "title-label", "middle");
  });

  opponents.forEach((opponent, rowIndex) => {
    const y = margin.top + rowIndex * cellHeight + cellHeight / 2;
    drawText(svg, margin.left - 12, y + 4, opponent, "title-label", "end");
  });

  kryptoniteMatrix.forEach((cell) => {
    const row = opponents.indexOf(cell.opponent);
    const col = seasons.indexOf(cell.season);
    const x = margin.left + col * cellWidth;
    const y = margin.top + row * cellHeight;
    const rect = createSvgNode("rect", {
      x,
      y,
      width: cellWidth - 4,
      height: cellHeight - 4,
      rx: 12,
      fill: heatColor(cell.goals),
    });
    rect.addEventListener("mousemove", (event) => {
      showTooltip(
        `<strong>${cell.opponent}</strong><br>Season: ${cell.season}<br>Barcelona goals: ${cell.goals.toFixed(1)}`,
        event,
      );
    });
    rect.addEventListener("mouseleave", hideTooltip);
    svg.appendChild(rect);
    drawText(svg, x + cellWidth / 2, y + cellHeight / 2 + 4, cell.goals.toFixed(1), "label", "middle");
  });

  drawText(svg, width / 2, 24, "Opponents that suppress Barcelona's attack", "title-label", "middle");
  summary.textContent =
    `${opponents[0]} appears as the most difficult opponent in the sample because Barcelona's goal output stays lowest across seasons.`;
}

function renderBenchmarkChart() {
  const svg = document.querySelector("#chart-benchmark");
  const summary = document.querySelector("#benchmark-summary");
  clearSvg(svg);

  const width = 740;
  const height = 420;
  const margin = { top: 30, right: 30, bottom: 60, left: 70 };

  [54, 56, 58, 60, 62, 64].forEach((value) => {
    const x = scaleLinear(value, 54, 64, margin.left, width - margin.right);
    svg.appendChild(createSvgNode("line", { x1: x, y1: margin.top, x2: x, y2: height - margin.bottom, class: "gridline" }));
    drawText(svg, x, height - 32, `${value}%`, "label", "middle");
  });

  [1.8, 2.0, 2.2, 2.4, 2.6].forEach((value) => {
    const y = scaleLinear(value, 1.8, 2.6, height - margin.bottom, margin.top);
    svg.appendChild(createSvgNode("line", { x1: margin.left, y1: y, x2: width - margin.right, y2: y, class: "gridline" }));
    drawText(svg, margin.left - 12, y + 4, `${value.toFixed(1)}`, "label", "end");
  });

  const avgPossession = benchmarkClubs.reduce((sum, club) => sum + club.possession, 0) / benchmarkClubs.length;
  const avgGoals = benchmarkClubs.reduce((sum, club) => sum + club.goalsPerGame, 0) / benchmarkClubs.length;
  const xRef = scaleLinear(avgPossession, 54, 64, margin.left, width - margin.right);
  const yRef = scaleLinear(avgGoals, 1.8, 2.6, height - margin.bottom, margin.top);
  svg.appendChild(createSvgNode("line", { x1: xRef, y1: margin.top, x2: xRef, y2: height - margin.bottom, class: "reference-line" }));
  svg.appendChild(createSvgNode("line", { x1: margin.left, y1: yRef, x2: width - margin.right, y2: yRef, class: "reference-line" }));

  benchmarkClubs.forEach((club) => {
    const x = scaleLinear(club.possession, 54, 64, margin.left, width - margin.right);
    const y = scaleLinear(club.goalsPerGame, 1.8, 2.6, height - margin.bottom, margin.top);
    const radius = 7 + club.pointsPerGame * 3;
    const isBarcelona = club.club === "Barcelona";
    const color = isBarcelona ? palette.accent : palette.accent2;
    const circle = createSvgNode("circle", {
      cx: x,
      cy: y,
      r: radius,
      fill: color,
      opacity: isBarcelona ? 0.95 : 0.76,
    });
    circle.addEventListener("mousemove", (event) => {
      showTooltip(
        `<strong>${club.club}</strong><br>Possession: ${club.possession}%<br>Goals per game: ${club.goalsPerGame}<br>Points per game: ${club.pointsPerGame}`,
        event,
      );
    });
    circle.addEventListener("mouseleave", hideTooltip);
    svg.appendChild(circle);
    drawText(svg, x, y - radius - 8, club.club, isBarcelona ? "title-label" : "label", "middle");
  });

  drawText(svg, width / 2, 20, "Benchmarking against elite clubs", "title-label", "middle");
  drawText(svg, width / 2, height - 12, "Average possession", "label", "middle");
  drawText(svg, 20, height / 2, "Goals per game", "label");

  const barca = benchmarkClubs.find((club) => club.club === "Barcelona");
  summary.textContent =
    `Barcelona combines above-average possession (${barca.possession}%) with solid attacking output, but the benchmark view also shows that teams like Manchester City and Real Madrid convert control into slightly stronger end results.`;
}

function init() {
  mountCards();
  renderPossessionChart();
  renderScoutingChart();
  renderKryptoniteChart();
  renderBenchmarkChart();

  const venueFilter = document.querySelector("#venue-filter");
  venueFilter.addEventListener("change", (event) => {
    renderPossessionChart(event.target.value);
  });
}

init();
