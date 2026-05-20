from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
RAW = ROOT / "VDS2526 Football"
CHARTS.mkdir(parents=True, exist_ok=True)

MASTER_PATH = DATA / "master_matches.csv"
BARCA_PATH = DATA / "barcelona_matches.csv"
CHART_BG = "#eceff1"
GRID_COLOR = "#dde4ea"
AXIS_COLOR = "#d4dbe2"
PLOTLY_CONFIG = {
    "responsive": True,
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": False,
}


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    master = pd.read_csv(MASTER_PATH)
    barca = pd.read_csv(BARCA_PATH)

    numeric_cols_master = [
        "home_team_goal",
        "away_team_goal",
        "home_possession",
        "away_possession",
        "home_shots_on",
        "away_shots_on",
        "home_shots_off",
        "away_shots_off",
    ]
    numeric_cols_barca = [
        "barca_goals",
        "opponent_goals",
        "barca_possession",
        "opponent_possession",
        "barca_shots_on",
        "opponent_shots_on",
        "barca_shots_off",
        "opponent_shots_off",
        "barca_total_shots",
        "opponent_total_shots",
        "barca_shot_accuracy",
        "barca_points",
    ]

    for col in numeric_cols_master:
        if col in master.columns:
            master[col] = pd.to_numeric(master[col], errors="coerce")

    for col in numeric_cols_barca:
        if col in barca.columns:
            barca[col] = pd.to_numeric(barca[col], errors="coerce")

    return master, barca


def write_chart(fig: go.Figure, filename: str) -> None:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="Inter, Arial, sans-serif", color="#1f2a30"),
        hoverlabel=dict(
            bgcolor="rgba(255,255,255,0.96)",
            bordercolor="#c7d0d9",
            font=dict(family="Inter, Arial, sans-serif", size=12, color="#1f2a30"),
            align="left",
        ),
        margin=dict(l=55, r=30, t=70, b=55),
        dragmode="pan",
        xaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            linecolor=AXIS_COLOR,
            zerolinecolor=GRID_COLOR,
            showline=True,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            linecolor=AXIS_COLOR,
            zerolinecolor=GRID_COLOR,
            showline=True,
        ),
    )
    fig.write_html(
        CHARTS / filename,
        full_html=True,
        include_plotlyjs="cdn",
        config=PLOTLY_CONFIG,
    )


def build_act1(barca: pd.DataFrame) -> None:
    act1 = barca.dropna(subset=["barca_possession", "barca_result"]).copy()
    act1["date"] = pd.to_datetime(act1["date"], errors="coerce", dayfirst=True)
    act1["date_label"] = act1["date"].dt.strftime("%d/%m/%Y")
    act1["score_label"] = (
        act1["barca_goals"].fillna(0).astype(int).astype(str)
        + "-"
        + act1["opponent_goals"].fillna(0).astype(int).astype(str)
    )

    result_order = ["Draw", "Win", "Loss"]
    palette = {
        "Loss": "#bb4d4d",
        "Win": "#2f7d60",
        "Draw": "#d6a74d",
    }
    basic_hover = (
        "<b>%{customdata[3]}</b><br>"
        "Result: %{y}<br>"
        "Venue: %{customdata[2]}<br>"
        "Season: %{customdata[0]}<br>"
        "Score: %{customdata[4]}<br>"
        "Barcelona possession: %{x:.1f}%<extra></extra>"
    )
    extended_hover = (
        "<b>%{customdata[3]}</b><br>"
        "Result: %{y}<br>"
        "Venue: %{customdata[2]}<br>"
        "Season: %{customdata[0]}<br>"
        "Score: %{customdata[4]}<br>"
        "Barcelona possession: %{x:.1f}%<br>"
        "Barcelona shots on: %{customdata[6]}<br>"
        "Barcelona shots off: %{customdata[7]}<br>"
        "Barcelona total shots: %{customdata[8]}<extra></extra>"
    )

    fig = go.Figure()
    trace_indices = {"All": [], "Home": [], "Away": []}
    all_showlegend = []

    for venue_key, venue_filter in [("All", None), ("Home", "Home"), ("Away", "Away")]:
        for result in ["Loss", "Win", "Draw"]:
            subset = act1[act1["barca_result"] == result].copy()
            if venue_filter is not None:
                subset = subset[subset["venue"] == venue_filter].copy()

            fig.add_trace(
                go.Box(
                    x=subset["barca_possession"],
                    y=subset["barca_result"],
                    name=result,
                    orientation="h",
                    boxpoints="all",
                    jitter=0.25,
                    pointpos=0,
                    marker=dict(
                        color=palette[result],
                        line=dict(color="white", width=0.5),
                        size=7,
                    ),
                    customdata=subset[
                        [
                            "season",
                            "date_label",
                            "venue",
                            "opponent_name",
                            "score_label",
                            "league_name",
                            "barca_shots_on",
                            "barca_shots_off",
                            "barca_total_shots",
                            "barca_goals",
                            "opponent_goals",
                        ]
                    ].to_numpy(),
                    hovertemplate=basic_hover,
                    visible=(venue_key == "All"),
                    showlegend=(venue_key == "All"),
                    legendgroup=result,
                )
            )
            trace_indices[venue_key].append(len(fig.data) - 1)
            all_showlegend.append(venue_key == "All")

    def venue_visibility(key: str) -> list[bool]:
        visible = [False] * len(fig.data)
        for idx in trace_indices[key]:
            visible[idx] = True
        return visible

    def venue_showlegend(key: str) -> list[bool]:
        showlegend = [False] * len(fig.data)
        for idx in trace_indices[key]:
            showlegend[idx] = True
        return showlegend

    fig.update_layout(
        title=dict(
            text="Barcelona Possession Distribution by Match Result",
            x=0.05,
        ),
        xaxis_title="Barcelona possession (%)",
        yaxis=dict(
            title="Match Result",
            categoryorder="array",
            categoryarray=result_order,
        ),
        boxmode="overlay",
        annotations=[
            dict(
                x=75.0,
                y="Loss",
                text="High possession can still end in defeat",
                showarrow=True,
                arrowhead=2,
                ax=40,
                ay=-40,
                bgcolor="rgba(255, 255, 255, 0.9)",
                bordercolor="#bb4d4d",
                borderwidth=1,
                borderpad=4,
            )
        ],
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=0.82,
                y=0.99,
                xanchor="right",
                yanchor="top",
                showactive=True,
                buttons=[
                    dict(
                        label="All matches",
                        method="update",
                        args=[
                            {"visible": venue_visibility("All"), "showlegend": venue_showlegend("All")},
                            {},
                        ],
                    ),
                    dict(
                        label="Home matches",
                        method="update",
                        args=[
                            {"visible": venue_visibility("Home"), "showlegend": venue_showlegend("Home")},
                            {},
                        ],
                    ),
                    dict(
                        label="Away matches",
                        method="update",
                        args=[
                            {"visible": venue_visibility("Away"), "showlegend": venue_showlegend("Away")},
                            {},
                        ],
                    ),
                ],
            ),
            dict(
                type="dropdown",
                direction="down",
                x=0.99,
                y=0.99,
                xanchor="right",
                yanchor="top",
                showactive=True,
                buttons=[
                    dict(
                        label="Basic hover",
                        method="restyle",
                        args=[{"hovertemplate": [basic_hover] * len(fig.data)}],
                    ),
                    dict(
                        label="Hover + shots",
                        method="restyle",
                        args=[{"hovertemplate": [extended_hover] * len(fig.data)}],
                    ),
                ],
            ),
        ],
    )
    write_chart(fig, "act1_boxplot.html")


def patch_chart_interactivity(filename: str) -> None:
    chart_path = CHARTS / filename
    if not chart_path.exists():
        return

    html = chart_path.read_text(encoding="utf-8")
    html = re.sub(
        r'\{"responsive": true[^}]*\}',
        '{"responsive": true, "displayModeBar": true, "displaylogo": false, "scrollZoom": false}',
        html,
        count=1,
    )
    html = html.replace('"dragmode":"zoom"', '"dragmode":"pan"')
    chart_path.write_text(html, encoding="utf-8")


def patch_act2_skill_legend(filename: str) -> None:
    chart_path = CHARTS / filename
    if not chart_path.exists():
        return

    html = chart_path.read_text(encoding="utf-8")
    if "act2-controls" in html:
        return

    script = """
<script>
(function () {
  const gd = document.querySelector('.plotly-graph-div');
  if (!gd) return;
  const wrapper = document.createElement('div');
  wrapper.id = 'act2-controls';
  wrapper.style.cssText = 'display:flex;flex-wrap:nowrap;gap:6px;justify-content:flex-start;align-items:center;margin:6px 0 10px;padding:0 14px 0 34px;box-sizing:border-box;max-width:100%;font-family:Inter,Arial,sans-serif;overflow:visible;';

  function makeControl(labelText, id) {
    const label = document.createElement('label');
    label.style.cssText = 'display:flex;align-items:center;gap:4px;font-size:11px;color:#334155;background:rgba(255,255,255,0.75);border:1px solid #c7d0d9;border-radius:8px;padding:4px 8px;white-space:nowrap;';
    const span = document.createElement('span');
    span.textContent = labelText;
    span.style.fontWeight = '600';
    const select = document.createElement('select');
    select.id = id;
    select.style.cssText = 'border:1px solid #b9c4cf;border-radius:6px;background:#f8fafc;color:#1f2a30;padding:3px 6px;font-size:11px;';
    label.appendChild(span);
    label.appendChild(select);
    wrapper.appendChild(label);
    return select;
  }

  const playerSel = makeControl('Player', 'act2-player');
  const shortlistSel = makeControl('Shortlist', 'act2-shortlist');
  const leagueSel = makeControl('League', 'act2-league');
  const positionSel = makeControl('Position', 'act2-position');
  const skillSel = makeControl('Skill', 'act2-skill');

  const plotContainer = gd.parentElement;
  const titleNode = plotContainer.querySelector('.gtitle');
  const titleGroup = titleNode ? titleNode.parentElement : null;
  if (titleGroup && titleGroup.parentElement) {
    const titleBox = titleGroup.getBoundingClientRect();
    const plotBox = plotContainer.getBoundingClientRect();
    wrapper.style.margin = (Math.max(12, titleBox.bottom - plotBox.top + 10)) + 'px 0 10px';
  }
  plotContainer.parentElement.insertBefore(wrapper, plotContainer);

  const traceMeta = gd.data.map((trace, idx) => ({
    idx,
    name: String(trace.name || ''),
    meta: trace.meta || {},
  }));

  const realTraces = traceMeta.filter(t => !t.meta.control);
  const players = [...new Set(realTraces.map(t => t.meta.player))].sort();
  const leagues = [...new Set(realTraces.map(t => t.meta.league))].sort();
  const positions = [...new Set(realTraces.map(t => t.meta.position))].sort();

  function fillSelect(select, values, allLabel) {
    select.innerHTML = '';
    const allOpt = document.createElement('option');
    allOpt.value = 'All';
    allOpt.textContent = allLabel;
    select.appendChild(allOpt);
    values.forEach(v => {
      const opt = document.createElement('option');
      opt.value = v;
      opt.textContent = v;
      select.appendChild(opt);
    });
  }

  fillSelect(playerSel, players, 'All players');
  shortlistSel.innerHTML = '<option value="5">Top 5</option><option value="10">Top 10</option><option value="15">Top 15</option><option value="20">Top 20</option>';
  fillSelect(leagueSel, leagues, 'All leagues');
  fillSelect(positionSel, positions, 'All positions');
  skillSel.innerHTML = '<option value="both">Both skills</option><option value="short">Short passing</option><option value="vision">Vision</option>';

  const filters = { player: 'All', shortlist: '5', league: 'All', position: 'All', skill: 'both' };
  shortlistSel.value = '5';

  function applyFilters() {
    gd.data.forEach((trace, idx) => {
      const meta = trace.meta || {};
      if (meta.control) {
        Plotly.restyle(gd, {visible: true}, [idx]);
        return;
      }
      let visible = true;
      if (filters.player !== 'All' && meta.player !== filters.player) visible = false;
      if (filters.league !== 'All' && meta.league !== filters.league) visible = false;
      if (filters.position !== 'All' && meta.position !== filters.position) visible = false;
      if (Number(meta.player_rank) > Number(filters.shortlist)) visible = false;
      if (filters.skill === 'short' && meta.skill !== 'short') visible = false;
      if (filters.skill === 'vision' && meta.skill !== 'vision') visible = false;
      Plotly.restyle(gd, {visible: visible}, [idx]);
    });
  }

  [playerSel, shortlistSel, leagueSel, positionSel, skillSel].forEach(sel => {
    sel.addEventListener('change', () => {
      filters.player = playerSel.value;
      filters.shortlist = shortlistSel.value;
      filters.league = leagueSel.value;
      filters.position = positionSel.value;
      filters.skill = skillSel.value;
      applyFilters();
    });
  });

  applyFilters();
})();
</script>
"""

    html = html.replace("</body>", script + "\n</body>")
    chart_path.write_text(html, encoding="utf-8")


def season_from_date(dt: pd.Timestamp) -> str:
    year = dt.year
    return f"{year}/{year + 1}" if dt.month >= 7 else f"{year - 1}/{year}"


def build_task2_dataset() -> pd.DataFrame:
    target_seasons = ["2013/2014", "2014/2015", "2015/2016"]
    player = pd.read_csv(RAW / "Player.csv")
    attrs = pd.read_csv(RAW / "Player_Attributes.csv")
    match = pd.read_csv(RAW / "Match.csv")
    team = pd.read_csv(RAW / "Team.csv")
    position_ref = pd.read_csv(RAW / "PositionReference.csv")
    barca_id = int(team.loc[team["team_long_name"] == "FC Barcelona", "team_api_id"].iloc[0])
    player_season_rows: list[dict] = []
    position_rows: list[dict] = []
    home_cols = [f"home_player_{i}" for i in range(1, 12)]
    away_cols = [f"away_player_{i}" for i in range(1, 12)]

    for _, row in match.iterrows():
        for i, col in enumerate(home_cols, start=1):
            value = row[col]
            if pd.notna(value) and value > 0:
                player_season_rows.append(
                    {
                        "player_api_id": int(value),
                        "season": row["season"],
                        "team_api_id": int(row["home_team_api_id"]),
                        "league_id": int(row["league_id"]),
                    }
                )
                pos_x = row.get(f"home_player_X{i}")
                pos_y = row.get(f"home_player_Y{i}")
                if pd.notna(pos_x) and pd.notna(pos_y):
                    position_rows.append(
                        {
                            "player_api_id": int(value),
                            "season": row["season"],
                            "player_pos_x": int(pos_x),
                            "player_pos_y": int(pos_y),
                        }
                    )
        for i, col in enumerate(away_cols, start=1):
            value = row[col]
            if pd.notna(value) and value > 0:
                player_season_rows.append(
                    {
                        "player_api_id": int(value),
                        "season": row["season"],
                        "team_api_id": int(row["away_team_api_id"]),
                        "league_id": int(row["league_id"]),
                    }
                )
                pos_x = row.get(f"away_player_X{i}")
                pos_y = row.get(f"away_player_Y{i}")
                if pd.notna(pos_x) and pd.notna(pos_y):
                    position_rows.append(
                        {
                            "player_api_id": int(value),
                            "season": row["season"],
                            "player_pos_x": int(pos_x),
                            "player_pos_y": int(pos_y),
                        }
                    )

    player_season_appearances = (
        pd.DataFrame(player_season_rows)
        .groupby(["player_api_id", "season", "team_api_id", "league_id"], as_index=False)
        .size()
        .rename(columns={"size": "appearances"})
    )
    player_team_seasons = (
        player_season_appearances.sort_values(
            ["player_api_id", "season", "appearances"],
            ascending=[True, True, False],
        )
        .drop_duplicates(["player_api_id", "season"])
        .copy()
    )
    player_team_seasons = player_team_seasons[player_team_seasons["team_api_id"] != barca_id].copy()
    player_team_seasons = player_team_seasons[
        player_team_seasons["season"].isin(target_seasons)
    ].copy()

    player_positions = pd.DataFrame(position_rows)
    player_positions = player_positions[player_positions["season"].isin(target_seasons)].copy()
    player_positions = player_positions.merge(
        position_ref[["player_pos_x", "player_pos_y", "role_xy"]],
        on=["player_pos_x", "player_pos_y"],
        how="left",
    )
    player_positions = player_positions.dropna(subset=["role_xy"]).copy()
    player_positions = (
        player_positions.groupby(["player_api_id", "season", "role_xy"], as_index=False)
        .size()
        .rename(columns={"size": "position_appearances"})
        .sort_values(
            ["player_api_id", "season", "position_appearances"],
            ascending=[True, True, False],
        )
        .drop_duplicates(["player_api_id", "season"])
        .rename(columns={"role_xy": "position_label"})
    )

    team_lookup = team[["team_api_id", "team_long_name"]].rename(
        columns={"team_long_name": "team_name"}
    )
    league_lookup = pd.read_csv(RAW / "League.csv")[["id", "name"]].rename(
        columns={"id": "league_id", "name": "league_name"}
    )
    player_team_seasons = player_team_seasons.merge(team_lookup, on="team_api_id", how="left")
    player_team_seasons = player_team_seasons.merge(league_lookup, on="league_id", how="left")
    player_team_seasons = player_team_seasons.merge(
        player_positions[["player_api_id", "season", "position_label"]],
        on=["player_api_id", "season"],
        how="left",
    )
    player_team_seasons["position_label"] = player_team_seasons["position_label"].fillna("Unknown")

    attrs["date"] = pd.to_datetime(attrs["date"])
    attrs["season"] = attrs["date"].map(season_from_date)
    attrs = attrs[attrs["season"].isin(target_seasons)].copy()

    player_meta = player[["player_api_id", "player_name", "birthday"]].copy()
    player_meta["birthday"] = pd.to_datetime(player_meta["birthday"])
    player_meta["age_at_record"] = pd.NA

    merged = attrs.merge(player_meta, on="player_api_id", how="inner")
    merged["age_at_record"] = ((merged["date"] - merged["birthday"]).dt.days / 365.25)
    merged = merged.merge(player_team_seasons, on=["player_api_id", "season"], how="inner")

    # Task 2 method:
    # 1. keep players from all clubs in the dataset except Barcelona itself
    # 2. calculate age from birthday and keep under-25 records
    # 3. group by player_name and date
    # 4. extract short_passing and vision
    # 5. roll up to season level and keep only players with a positive trend
    #    across their last 3 seasons
    merged = merged.loc[merged["age_at_record"] < 25, [
        "player_api_id",
        "player_name",
        "team_name",
        "league_name",
        "position_label",
        "date",
        "season",
        "age_at_record",
        "short_passing",
        "vision",
        "overall_rating",
    ]].copy()

    date_level = (
        merged.groupby(
            ["player_api_id", "player_name", "team_name", "league_name", "position_label", "date", "season"],
            as_index=False,
        )[["short_passing", "vision", "overall_rating", "age_at_record"]].mean()
    )

    season_level = (
        date_level.groupby(
            ["player_api_id", "player_name", "team_name", "league_name", "position_label", "season"],
            as_index=False,
        )[["short_passing", "vision", "overall_rating", "age_at_record"]].mean()
    )

    trend_rows = []
    for (pid, pname), player_df in season_level.groupby(["player_api_id", "player_name"]):
        player_df = player_df.sort_values("season").copy()
        if player_df["season"].nunique() < 3:
            continue
        if sorted(player_df["season"].unique().tolist()) != target_seasons:
            continue
        last_three = player_df.tail(3)
        sp = last_three["short_passing"].tolist()
        vis = last_three["vision"].tolist()
        short_positive = sp[2] > sp[0]
        vision_positive = vis[2] > vis[0]
        if short_positive and vision_positive:
            growth = (sp[2] - sp[0]) + (vis[2] - vis[0])
            trend_rows.append(
                {
                    "player_api_id": pid,
                    "player_name": pname,
                    "growth": growth,
                    "short_growth": sp[2] - sp[0],
                    "vision_growth": vis[2] - vis[0],
                    "latest_season": last_three["season"].iloc[-1],
                }
            )

    trend_df = pd.DataFrame(trend_rows).sort_values(
        ["growth", "latest_season"], ascending=[False, False]
    )
    selected_ids = trend_df.head(20)["player_api_id"].tolist()

    task2_df = season_level[season_level["player_api_id"].isin(selected_ids)].copy()
    return task2_df


def build_act2() -> None:
    task2_df = build_task2_dataset()
    target_seasons = sorted(task2_df["season"].unique())
    player_growth = (
        task2_df.sort_values(["player_name", "season"])
        .groupby("player_name")
        .agg(
            short_start=("short_passing", "first"),
            short_end=("short_passing", "last"),
            vision_start=("vision", "first"),
            vision_end=("vision", "last"),
            team_name=("team_name", "last"),
            league_name=("league_name", "last"),
            position_label=("position_label", lambda s: s.mode().iat[0] if not s.mode().empty else s.iloc[-1]),
        )
    )
    player_growth["growth"] = (
        player_growth["short_end"] + player_growth["vision_end"]
        - player_growth["short_start"] - player_growth["vision_start"]
    )
    player_order = player_growth.sort_values("growth", ascending=False).index.tolist()
    palette = qualitative.Plotly + qualitative.Safe + qualitative.Vivid

    fig = go.Figure()
    for idx, player_name in enumerate(player_order):
        color = palette[idx % len(palette)]
        player_df = task2_df[task2_df["player_name"] == player_name].sort_values("season")
        team_name = player_df["team_name"].iloc[-1]
        league_name = player_df["league_name"].iloc[-1]
        position_label = player_df["position_label"].mode().iat[0] if not player_df["position_label"].mode().empty else player_df["position_label"].iloc[-1]
        fig.add_trace(
            go.Scatter(
                x=player_df["season"],
                y=player_df["short_passing"],
                mode="lines+markers",
                name=player_name,
                legendgroup=player_name,
                line=dict(color=color, width=3),
                marker=dict(size=8),
                meta={
                    "player": player_name,
                    "team": team_name,
                    "league": league_name,
                    "position": position_label,
                    "skill": "short",
                    "player_rank": idx + 1,
                },
                hovertemplate=(
                    f"<b>{player_name}</b><br>"
                    f"Club: {team_name}<br>"
                    f"League: {league_name}<br>"
                    f"Position: {position_label}<br>"
                    "Skill: Short passing<br>"
                    "Season: %{x}<br>"
                    "Value: %{y:.1f}<extra></extra>"
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=player_df["season"],
                y=player_df["vision"],
                mode="lines+markers",
                name=f"{player_name} vision",
                legendgroup=player_name,
                showlegend=False,
                line=dict(color=color, width=3, dash="dash"),
                marker=dict(size=7),
                meta={
                    "player": player_name,
                    "team": team_name,
                    "league": league_name,
                    "position": position_label,
                    "skill": "vision",
                    "player_rank": idx + 1,
                },
                hovertemplate=(
                    f"<b>{player_name}</b><br>"
                    f"Club: {team_name}<br>"
                    f"League: {league_name}<br>"
                    f"Position: {position_label}<br>"
                    "Skill: Vision<br>"
                    "Season: %{x}<br>"
                    "Value: %{y:.1f}<extra></extra>"
                ),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="#334155", width=3),
            name="Short passing",
            hoverinfo="skip",
            meta={"control": "skill-key", "skill": "short"},
            showlegend=True,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="#334155", width=3, dash="dash"),
            name="Vision",
            hoverinfo="skip",
            meta={"control": "skill-key", "skill": "vision"},
            showlegend=True,
        )
    )

    fig.update_layout(
        title="Scouting under-25 hidden gems across European leagues",
        xaxis_title="Season",
        yaxis_title="Attribute value (0-100)",
        legend_title="Players",
        legend=dict(groupclick="togglegroup"),
        title_x=0.5,
        margin=dict(l=70, r=40, t=90, b=60),
    )
    fig.update_xaxes(categoryorder="array", categoryarray=target_seasons)
    fig.update_yaxes(range=[0, 100])
    write_chart(fig, "act2_hidden_gems.html")
    patch_act2_skill_legend("act2_hidden_gems.html")


def build_task3_dataset() -> pd.DataFrame:
    match = pd.read_csv(RAW / "Match.csv")
    team = pd.read_csv(RAW / "Team.csv")

    team_lookup = team[["team_api_id", "team_long_name"]].drop_duplicates().copy()
    home_lookup = team_lookup.rename(
        columns={
            "team_api_id": "home_team_api_id",
            "team_long_name": "home_team_name",
        }
    )
    away_lookup = team_lookup.rename(
        columns={
            "team_api_id": "away_team_api_id",
            "team_long_name": "away_team_name",
        }
    )

    match = match.merge(home_lookup, on="home_team_api_id", how="left")
    match = match.merge(away_lookup, on="away_team_api_id", how="left")

    barca_name = "FC Barcelona"
    barca_matches = match[
        (match["home_team_name"] == barca_name) | (match["away_team_name"] == barca_name)
    ].copy()

    barca_matches["opponent_team_name"] = barca_matches["home_team_name"]
    barca_matches.loc[
        barca_matches["home_team_name"] == barca_name, "opponent_team_name"
    ] = barca_matches["away_team_name"]

    barca_matches["barca_goals"] = barca_matches["away_team_goal"]
    barca_matches.loc[
        barca_matches["home_team_name"] == barca_name, "barca_goals"
    ] = barca_matches["home_team_goal"]

    task3_df = (
        barca_matches.groupby(["opponent_team_name", "season"], as_index=False)
        .agg(avg_barca_goals=("barca_goals", "mean"))
    )
    return task3_df

def build_act3() -> None:
    heat_df = build_task3_dataset()
    recurring_opponents = (
        heat_df.groupby("opponent_team_name")["season"]
        .nunique()
        .loc[lambda s: s >= 3]
        .index
    )
    heat_df = heat_df[heat_df["opponent_team_name"].isin(recurring_opponents)].copy()
    opponent_order = (
        heat_df.groupby("opponent_team_name")["avg_barca_goals"]
        .mean()
        .sort_values()
        .head(12)
        .index
    )
    
    heat_df = heat_df[heat_df["opponent_team_name"].isin(opponent_order)]
    pivot_df = heat_df.pivot(
        index="opponent_team_name",
        columns="season",
        values="avg_barca_goals"
    )
    
    pivot_df = pivot_df.loc[list(opponent_order)]
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Season", y="Opponent team", color="Avg Barça goals"),
        x=pivot_df.columns,
        y=pivot_df.index,
        text_auto=".2f", # type: ignore
        aspect="auto",
        color_continuous_scale=[
            [0.0, "#f7fbff"], 
            [0.35, "#c6dbef"],
            [0.70, "#4292c6"],
            [1.0, "#08306b"],
        ],
        title="Barcelona goals by opponent and season",
    )
    fig.update_layout(
        plot_bgcolor="#e9ecef", 
        xaxis_title="Season",
        yaxis_title="Opponent team",
        coloraxis_colorbar_title="Avg Barça goals",
    )
    write_chart(fig, "act3_kryptonite_heatmap.html")

def build_task4_elite_dataset(master: pd.DataFrame) -> pd.DataFrame:
    major_leagues = [
        "England Premier League",
        "Spain LIGA BBVA",
        "Italy Serie A",
        "Germany 1. Bundesliga",
        "France Ligue 1",
    ]

    home_rows = master[
        [
            "season",
            "league_name",
            "home_team_name",
            "away_team_name",
            "home_team_goal",
            "away_team_goal",
            "home_possession",
            "home_shots_on",
            "home_shots_off",
        ]
    ].copy()
    home_rows.columns = [
        "season",
        "league_name",
        "team_name",
        "opponent_name",
        "goals_for",
        "goals_against",
        "possession",
        "shots_on",
        "shots_off",
    ]
    home_rows["points"] = 0
    home_rows.loc[home_rows["goals_for"] > home_rows["goals_against"], "points"] = 3
    home_rows.loc[home_rows["goals_for"] == home_rows["goals_against"], "points"] = 1
    home_rows["match_result"] = "Draw"
    home_rows.loc[home_rows["goals_for"] > home_rows["goals_against"], "match_result"] = "Win"
    home_rows.loc[home_rows["goals_for"] < home_rows["goals_against"], "match_result"] = "Loss"

    away_rows = master[
        [
            "season",
            "league_name",
            "away_team_name",
            "home_team_name",
            "away_team_goal",
            "home_team_goal",
            "away_possession",
            "away_shots_on",
            "away_shots_off",
        ]
    ].copy()
    away_rows.columns = [
        "season",
        "league_name",
        "team_name",
        "opponent_name",
        "goals_for",
        "goals_against",
        "possession",
        "shots_on",
        "shots_off",
    ]
    away_rows["points"] = 0
    away_rows.loc[away_rows["goals_for"] > away_rows["goals_against"], "points"] = 3
    away_rows.loc[away_rows["goals_for"] == away_rows["goals_against"], "points"] = 1
    away_rows["match_result"] = "Draw"
    away_rows.loc[away_rows["goals_for"] > away_rows["goals_against"], "match_result"] = "Win"
    away_rows.loc[away_rows["goals_for"] < away_rows["goals_against"], "match_result"] = "Loss"

    club_matches = pd.concat([home_rows, away_rows], ignore_index=True)
    club_matches = club_matches[club_matches["league_name"].isin(major_leagues)].copy()
    club_matches["total_shots"] = club_matches["shots_on"].fillna(0) + club_matches["shots_off"].fillna(0)
    club_matches["shot_accuracy"] = club_matches["shots_on"] / club_matches["total_shots"].replace(0, pd.NA)

    season_summary = (
        club_matches.groupby(["season", "league_name", "team_name"], as_index=False)
        .agg(
            matches=("team_name", "size"),
            total_points=("points", "sum"),
            goals_for=("goals_for", "sum"),
            goals_against=("goals_against", "sum"),
            avg_possession=("possession", "mean"),
            goals_per_match=("goals_for", "mean"),
            points_per_match=("points", "mean"),
            avg_shot_accuracy=("shot_accuracy", "mean"),
            wins=("match_result", lambda s: (s == "Win").sum()),
        )
    )
    season_summary["goal_difference"] = season_summary["goals_for"] - season_summary["goals_against"]
    season_summary = season_summary.sort_values(
        ["season", "league_name", "total_points", "goal_difference", "goals_for"],
        ascending=[True, True, False, False, False],
    )
    season_summary["league_rank"] = (
        season_summary.groupby(["season", "league_name"]).cumcount() + 1
    )

    team_history = (
        season_summary.groupby(["team_name", "league_name"], as_index=False)
        .agg(
            seasons_observed=("season", "nunique"),
            top3_finishes=("league_rank", lambda s: (s <= 3).sum()),
            avg_possession=("avg_possession", "mean"),
            goals_per_match=("goals_per_match", "mean"),
            points_per_match=("points_per_match", "mean"),
            avg_shot_accuracy=("avg_shot_accuracy", "mean"),
            avg_rank=("league_rank", "mean"),
        )
    )
    team_history = team_history.sort_values(
        ["league_name", "top3_finishes", "avg_rank", "points_per_match", "goals_per_match"],
        ascending=[True, False, True, False, False],
    )
    team_history["league_elite_rank"] = (
        team_history.groupby("league_name").cumcount() + 1
    )

    benchmark = team_history[team_history["league_elite_rank"] <= 3].copy()
    benchmark["highlight"] = benchmark["team_name"].eq("FC Barcelona")
    return benchmark


# def build_act4(master: pd.DataFrame) -> None:
#     benchmark = build_task4_elite_dataset(master)
#     benchmark["label_name"] = benchmark["team_name"]
#     benchmark.loc[benchmark["team_name"] == "FC Barcelona", "label_name"] = ""

#     fig = px.scatter(
#         benchmark,
#         x="avg_possession",
#         y="goals_per_match",
#         size="points_per_match",
#         color="league_name",
#         text="label_name",
#         hover_name="team_name",
#         hover_data=["avg_shot_accuracy", "seasons_observed", "top3_finishes", "avg_rank"],
#         title="Task 4: Barcelona against top-3 teams from Europe's major leagues",
#     )
#     fig.update_traces(
#         textposition="top center",
#         textfont=dict(size=10),
#         marker=dict(line=dict(width=1, color="white"), opacity=0.72, sizeref=0.016),
#     )
#     barca_mask = benchmark["team_name"] == "FC Barcelona"
#     fig.add_trace(
#         go.Scatter(
#             x=benchmark.loc[barca_mask, "avg_possession"],
#             y=benchmark.loc[barca_mask, "goals_per_match"],
#             mode="markers+text",
#             text=benchmark.loc[barca_mask, "team_name"],
#             textposition="bottom center",
#             marker=dict(size=20, color="#912f40", symbol="diamond", line=dict(width=2, color="#ffffff")),
#             name="Barcelona highlight",
#             hovertemplate="FC Barcelona<br>Avg possession=%{x:.2f}<br>Goals per match=%{y:.2f}<extra></extra>",
#         )
#     )
#     fig.update_layout(
#         xaxis_title="Average possession (%)",
#         yaxis_title="Goals per match",
#         legend_title="League",
#         legend=dict(
#             orientation="v",
#             yanchor="top",
#             y=1,
#             xanchor="left",
#             x=1.02,
#         ),
#     )
#     write_chart(fig, "act4_european_benchmark.html")
def build_act4(master: pd.DataFrame) -> None:
    benchmark = build_task4_elite_dataset(master)
    barca_mask = benchmark["team_name"] == "FC Barcelona"
    barca_row = benchmark.loc[barca_mask].copy()
    peers = benchmark.loc[~barca_mask].copy()
    y_max = max(benchmark["goals_per_match"].max(), 0)

    fig = go.Figure()

    all_home = master[["home_team_name", "home_possession", "home_team_goal"]].copy()
    all_home.columns = ["team_name", "possession", "goals_for"]
    all_away = master[["away_team_name", "away_possession", "away_team_goal"]].copy()
    all_away.columns = ["team_name", "possession", "goals_for"]
    all_teams = pd.concat([all_home, all_away], ignore_index=True)
    all_teams = (
        all_teams.dropna(subset=["possession", "goals_for"])
        .groupby("team_name", as_index=False)
        .agg(
            avg_possession=("possession", "mean"),
            goals_per_match=("goals_for", "mean"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=all_teams["avg_possession"],
            y=all_teams["goals_per_match"],
            mode="markers",
            marker=dict(size=7, color="rgba(140, 146, 156, 0.38)"),
            name="All European teams",
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Avg possession: %{x:.2f}%<br>"
                "Goals per match: %{y:.2f}<extra>Background layer</extra>"
            ),
            customdata=all_teams[["team_name"]].to_numpy(),
        )
    )

    elite_fig = px.scatter(
        peers,
        x="avg_possession",
        y="goals_per_match",
        size="points_per_match",
        color="league_name",
        hover_name="team_name",
        custom_data=[
            "avg_shot_accuracy",
            "seasons_observed",
            "top3_finishes",
            "avg_rank",
            "league_name",
            "points_per_match",
        ],
        title="Task 4: Barcelona against top-3 teams from Europe's major leagues",
        size_max=18,
    )

    elite_fig.update_traces(
        marker_line_width=1.5,
        marker_line_color="white",
        opacity=0.85,
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "League: %{customdata[4]}<br>"
            "Avg possession: %{x:.2f}%<br>"
            "Goals per match: %{y:.2f}<br>"
            "Points per match: %{customdata[5]:.2f}<br>"
            "Shot accuracy: %{customdata[0]:.2f}<br>"
            "Seasons observed: %{customdata[1]}<br>"
            "Top-3 finishes: %{customdata[2]}<br>"
            "Average rank: %{customdata[3]:.2f}<extra>Elite benchmark</extra>"
        ),
    )
    for trace in elite_fig.data:
        fig.add_trace(trace)

    fig.add_trace(
        go.Scatter(
            x=barca_row["avg_possession"],
            y=barca_row["goals_per_match"],
            mode="markers",
            marker=dict(size=18, color="#912f40", symbol="diamond", line=dict(width=2, color="#ffffff")),
            name="Barcelona",
            showlegend=True,
            hovertemplate=(
                "<b>FC Barcelona</b><br>"
                "Avg possession: %{x:.2f}%<br>"
                "Goals per match: %{y:.2f}<br>"
                "Points per match: %{customdata[0]:.2f}<br>"
                "Shot accuracy: %{customdata[1]:.2f}<br>"
                "Seasons observed: %{customdata[2]}<br>"
                "Top-3 finishes: %{customdata[3]}<br>"
                "Average rank: %{customdata[4]:.2f}<extra>Barcelona highlight</extra>"
            ),
            customdata=barca_row[["points_per_match", "avg_shot_accuracy", "seasons_observed", "top3_finishes", "avg_rank"]].to_numpy(),
        )
    )

    fig.update_layout(
        title=dict(
            text="Task 4: Barcelona against top-3 teams from Europe's major leagues",
            x=0.5,
        ),
        xaxis_title="Average possession (%)",
        yaxis_title="Goals per match",
        yaxis=dict(range=[0, max(3.2, y_max + 0.25)]),
        legend_title="League",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            itemsizing="constant",
        ),
    )
    
    write_chart(fig, "act4_european_benchmark.html")


def main() -> None:
    master, barca = load_datasets()
    build_act1(barca)
    build_act2()
    build_act3()
    build_act4(master)
    patch_chart_interactivity("act1_boxplot.html")
    print(f"Saved charts to {CHARTS}")


if __name__ == "__main__":
    main()
