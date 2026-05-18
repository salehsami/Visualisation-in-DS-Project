from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import qualitative
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
RAW = ROOT / "VDS2526 Football"
CHARTS.mkdir(parents=True, exist_ok=True)

MASTER_PATH = DATA / "master_matches.csv"
BARCA_PATH = DATA / "barcelona_matches.csv"
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
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", color="#1f2a30"),
        margin=dict(l=55, r=30, t=70, b=55),
        dragmode="pan",
    )
    fig.write_html(
        CHARTS / filename,
        full_html=True,
        include_plotlyjs="cdn",
        config=PLOTLY_CONFIG,
    )


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


def season_from_date(dt: pd.Timestamp) -> str:
    year = dt.year
    return f"{year}/{year + 1}" if dt.month >= 7 else f"{year - 1}/{year}"


def build_task2_dataset() -> pd.DataFrame:
    player = pd.read_csv(RAW / "Player.csv")
    attrs = pd.read_csv(RAW / "Player_Attributes.csv")
    match = pd.read_csv(RAW / "Match.csv")
    team = pd.read_csv(RAW / "Team.csv")
    barca_id = int(team.loc[team["team_long_name"] == "FC Barcelona", "team_api_id"].iloc[0])

    barca_matches = match[
        (match["home_team_api_id"] == barca_id) | (match["away_team_api_id"] == barca_id)
    ].copy()
    player_season_rows: list[dict] = []
    home_cols = [f"home_player_{i}" for i in range(1, 12)]
    away_cols = [f"away_player_{i}" for i in range(1, 12)]
    for _, row in barca_matches.iterrows():
        lineup_cols = home_cols if row["home_team_api_id"] == barca_id else away_cols
        for col in lineup_cols:
            value = row[col]
            if pd.notna(value) and value > 0:
                player_season_rows.append(
                    {"player_api_id": int(value), "season": row["season"]}
                )

    barca_player_seasons = pd.DataFrame(player_season_rows).drop_duplicates()
    barca_player_ids = set(barca_player_seasons["player_api_id"])

    attrs["date"] = pd.to_datetime(attrs["date"])
    attrs["season"] = attrs["date"].map(season_from_date)

    player_meta = player[["player_api_id", "player_name", "birthday"]].copy()
    player_meta["birthday"] = pd.to_datetime(player_meta["birthday"])
    player_meta["age_at_record"] = pd.NA

    merged = attrs[attrs["player_api_id"].isin(barca_player_ids)].merge(
        player_meta, on="player_api_id", how="inner"
    )
    merged["age_at_record"] = ((merged["date"] - merged["birthday"]).dt.days / 365.25)
    merged = merged.merge(barca_player_seasons, on=["player_api_id", "season"], how="inner")

    # Task 2 method:
    # 1. keep only Barcelona players
    # 2. calculate age from birthday and keep under-25 records
    # 3. group by player_name and date
    # 4. extract short_passing and vision
    # 5. roll up to season level and keep only players with a positive trend
    #    across their last 3 seasons
    merged = merged.loc[merged["age_at_record"] < 25, [
        "player_api_id",
        "player_name",
        "date",
        "season",
        "age_at_record",
        "short_passing",
        "vision",
        "overall_rating",
    ]].copy()

    date_level = (
        merged.groupby(["player_api_id", "player_name", "date", "season"], as_index=False)[
            ["short_passing", "vision", "overall_rating", "age_at_record"]
        ]
        .mean()
    )

    season_level = (
        date_level.groupby(["player_api_id", "player_name", "season"], as_index=False)[
            ["short_passing", "vision", "overall_rating", "age_at_record"]
        ]
        .mean()
    )

    trend_rows = []
    for (pid, pname), player_df in season_level.groupby(["player_api_id", "player_name"]):
        player_df = player_df.sort_values("season").copy()
        if player_df["season"].nunique() < 3:
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
    selected_ids = trend_df["player_api_id"].tolist()

    task2_df = season_level[season_level["player_api_id"].isin(selected_ids)].copy()
    return task2_df


def build_act2(barca: pd.DataFrame) -> None:
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
        fig.add_trace(
            go.Scatter(
                x=player_df["season"],
                y=player_df["short_passing"],
                mode="lines+markers",
                name=player_name,
                legendgroup=player_name,
                line=dict(color=color, width=3),
                marker=dict(size=8),
                hovertemplate=f"{player_name}<br>Season=%{{x}}<br>Short passing=%{{y:.1f}}<extra></extra>",
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
                hovertemplate=f"{player_name}<br>Season=%{{x}}<br>Vision=%{{y:.1f}}<extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="#222222", width=3),
            name="Short passing",
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="lines",
            line=dict(color="#222222", width=3, dash="dash"),
            name="Vision",
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title="Task 2: Scouting Barça hidden gems under 25",
        xaxis_title="Season",
        yaxis_title="Attribute value (0-100)",
        legend_title="Players / skill key",
    )
    fig.update_xaxes(categoryorder="array", categoryarray=target_seasons)
    top_player = player_growth.sort_values("growth", ascending=False).reset_index().iloc[0]
    top_player_df = task2_df[task2_df["player_name"] == top_player["player_name"]].sort_values("season")
    last_row = top_player_df.iloc[-1]
    fig.add_annotation(
        x=last_row["season"],
        y=last_row["short_passing"],
        text=f"Strongest growth: {top_player['player_name']}",
        showarrow=True,
        ax=45,
        ay=-40,
        bgcolor="rgba(255,255,255,0.88)",
    )
    write_chart(fig, "act2_control_into_chances.html")


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


def build_act3(barca: pd.DataFrame) -> None:
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
    heat_df["opponent_team_name"] = pd.Categorical(
        heat_df["opponent_team_name"], categories=list(opponent_order), ordered=True
    )
    heat_df = heat_df.sort_values(["opponent_team_name", "season"])

    fig = px.density_heatmap(
        heat_df,
        x="season",
        y="opponent_team_name",
        z="avg_barca_goals",
        histfunc="avg",
        text_auto=".2f",
        color_continuous_scale=[
            [0.0, "#f9efe5"],
            [0.45, "#f0b690"],
            [0.75, "#d97d54"],
            [1.0, "#912f40"],
        ],
        title="Task 3: Barcelona goals by opponent and season",
    )
    fig.update_layout(
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
    benchmark["label_name"] = benchmark["team_name"]
    benchmark.loc[benchmark["team_name"] == "FC Barcelona", "label_name"] = ""

    # 1. TOP LAYER (ELITE TEAMS): Bubble Chart
    fig = px.scatter(
        benchmark,
        x="avg_possession",
        y="goals_per_match",
        size="points_per_match", 
        color="league_name",
        text="label_name",
        hover_name="team_name",
        hover_data=["avg_shot_accuracy", "seasons_observed", "top3_finishes", "avg_rank"],
        title="Task 4: Barcelona against top-3 teams vs Rest of Europe",
        size_max=18 
    )
    
    fig.update_traces(
        textposition="top center",
        textfont=dict(size=10),
        marker_line_width=1.5,
        marker_line_color="white",
        opacity=0.85
    )

    elite_traces = list(fig.data)
    fig.data = []

    # 2. BOTTOM LAYER (BACKGROUND): All European Teams
    try:
        all_teams = master.groupby("home_team_name").agg(
            avg_possession=("home_possession", "mean"), 
            goals_per_match=("home_team_goal", "mean") 
        ).reset_index()

        all_teams = all_teams.dropna(subset=["avg_possession", "goals_per_match"])

        fig.add_trace(
            go.Scatter(
                x=all_teams["avg_possession"],
                y=all_teams["goals_per_match"],
                mode="markers",
                marker=dict(size=6, color="lightgrey", opacity=0.4),
                name="All European Teams",
                hoverinfo="skip", 
            )
        )
    except KeyError as e:
        print(f"Background layer could not be drawn, check columns: {e}")

    for trace in elite_traces:
        fig.add_trace(trace)

    # 3. FOCUS POINT: FC Barcelona Highlight
    barca_mask = benchmark["team_name"] == "FC Barcelona"
    fig.add_trace(
        go.Scatter(
            x=benchmark.loc[barca_mask, "avg_possession"],
            y=benchmark.loc[barca_mask, "goals_per_match"],
            mode="markers+text",
            text=benchmark.loc[barca_mask, "team_name"],
            textposition="bottom center",
            marker=dict(size=20, color="#912f40", symbol="diamond", line=dict(width=2, color="#ffffff")),
            name="Barcelona highlight",
            hovertemplate="FC Barcelona<br>Avg possession=%{x:.2f}<br>Goals per match=%{y:.2f}<extra></extra>",
        )
    )

    # 4. VISUAL ADJUSTMENTS
    fig.update_layout(
        xaxis_title="Average possession (%)",
        yaxis_title="Goals per match",
        legend_title="Legend",
        plot_bgcolor="#f4f4f9", 
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
        ),
    )
    
    write_chart(fig, "act4_european_benchmark.html")


def main() -> None:
    master, barca = load_datasets()
    build_act2(barca)
    build_act3(barca)
    build_act4(master)
    patch_chart_interactivity("act1_boxplot.html")
    print(f"Saved charts to {CHARTS}")


if __name__ == "__main__":
    main()
