from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CHARTS = ROOT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

MASTER_PATH = DATA / "master_matches.csv"
BARCA_PATH = DATA / "barcelona_matches.csv"


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
    )
    fig.write_html(CHARTS / filename, full_html=True, include_plotlyjs="cdn")


def build_act1(barca: pd.DataFrame) -> None:
    chart_df = barca[barca["has_possession_data"]].copy()
    y_map = {"Loss": 0, "Draw": 1, "Win": 2}
    venue_offset = {"Home": -0.12, "Away": 0.12}
    chart_df["result_code"] = chart_df["barca_result"].map(y_map)
    chart_df["result_jitter"] = chart_df["result_code"] + chart_df["venue"].map(venue_offset).fillna(0)

    fig = px.scatter(
        chart_df,
        x="barca_possession",
        y="result_jitter",
        color="barca_result",
        symbol="venue",
        hover_data=[
            "season",
            "date",
            "opponent_name",
            "barca_goals",
            "opponent_goals",
            "barca_shots_on",
            "opponent_shots_on",
        ],
        color_discrete_map={"Win": "#2f7d60", "Draw": "#d6a74d", "Loss": "#bb4d4d"},
        title="Barcelona possession by result and venue",
    )
    fig.update_traces(marker=dict(size=10, line=dict(width=0.6, color="white")))
    fig.update_layout(
        xaxis_title="Barcelona possession (%)",
        yaxis_title="Match result",
        legend_title="Result / Venue",
    )
    fig.update_yaxes(
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=["Loss", "Draw", "Win"],
        range=[-0.5, 2.5],
    )
    write_chart(fig, "act1_possession_vs_result.html")


def build_act2(barca: pd.DataFrame) -> None:
    season_df = (
        barca.groupby("season", as_index=False)
        .agg(
            avg_possession=("barca_possession", "mean"),
            avg_total_shots=("barca_total_shots", "mean"),
            avg_goals=("barca_goals", "mean"),
            avg_shot_accuracy=("barca_shot_accuracy", "mean"),
            win_rate=("barca_result", lambda s: (s == "Win").mean()),
        )
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=season_df["season"],
            y=season_df["avg_total_shots"],
            name="Avg total shots",
            marker_color="#d97d54",
            hovertemplate="Season=%{x}<br>Avg shots=%{y:.2f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=season_df["season"],
            y=season_df["avg_goals"],
            name="Avg goals",
            mode="lines+markers",
            line=dict(color="#912f40", width=3),
            marker=dict(size=8),
            hovertemplate="Season=%{x}<br>Avg goals=%{y:.2f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=season_df["season"],
            y=season_df["avg_shot_accuracy"],
            name="Shot accuracy",
            mode="lines+markers",
            line=dict(color="#2f5d62", width=3, dash="dot"),
            marker=dict(size=8),
            hovertemplate="Season=%{x}<br>Shot accuracy=%{y:.2%}<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_layout(title="Turning control into chances: Barcelona by season", bargap=0.35)
    fig.update_yaxes(title_text="Shots / goals per match", secondary_y=False)
    fig.update_yaxes(title_text="Shot accuracy", tickformat=".0%", secondary_y=True)
    fig.update_xaxes(title_text="Season")
    write_chart(fig, "act2_control_into_chances.html")


def build_act3(barca: pd.DataFrame) -> None:
    heat_df = (
        barca.groupby(["opponent_name", "season"], as_index=False)
        .agg(avg_barca_goals=("barca_goals", "mean"))
    )
    opponent_order = (
        heat_df.groupby("opponent_name")["avg_barca_goals"]
        .mean()
        .sort_values()
        .head(12)
        .index
    )
    heat_df = heat_df[heat_df["opponent_name"].isin(opponent_order)].copy()
    heat_df["opponent_name"] = pd.Categorical(
        heat_df["opponent_name"], categories=list(opponent_order), ordered=True
    )
    heat_df = heat_df.sort_values(["opponent_name", "season"])

    fig = px.density_heatmap(
        heat_df,
        x="season",
        y="opponent_name",
        z="avg_barca_goals",
        histfunc="avg",
        text_auto=".2f",
        color_continuous_scale=[
            [0.0, "#f9efe5"],
            [0.45, "#f0b690"],
            [0.75, "#d97d54"],
            [1.0, "#912f40"],
        ],
        title="Opponents that suppress Barcelona's attack",
    )
    fig.update_layout(xaxis_title="Season", yaxis_title="Opponent", coloraxis_colorbar_title="Avg goals")
    write_chart(fig, "act3_kryptonite_heatmap.html")


def build_act4(master: pd.DataFrame) -> None:
    home_rows = master[
        ["season", "league_name", "home_team_name", "away_team_name", "home_team_goal", "away_team_goal", "home_possession", "home_shots_on", "home_shots_off"]
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

    away_rows = master[
        ["season", "league_name", "away_team_name", "home_team_name", "away_team_goal", "home_team_goal", "away_possession", "away_shots_on", "away_shots_off"]
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

    club_matches = pd.concat([home_rows, away_rows], ignore_index=True)
    club_matches["total_shots"] = club_matches["shots_on"].fillna(0) + club_matches["shots_off"].fillna(0)
    club_matches["shot_accuracy"] = club_matches["shots_on"] / club_matches["total_shots"].replace(0, pd.NA)

    elite_clubs = [
        "FC Barcelona",
        "Real Madrid CF",
        "Atlético Madrid",
        "FC Bayern Munich",
        "Manchester City",
        "Manchester United",
        "Arsenal",
        "Chelsea",
        "Liverpool",
        "Juventus",
        "Inter",
        "Milan",
        "Paris Saint-Germain",
    ]

    benchmark = (
        club_matches[club_matches["team_name"].isin(elite_clubs)]
        .groupby(["team_name", "league_name"], as_index=False)
        .agg(
            avg_possession=("possession", "mean"),
            goals_per_match=("goals_for", "mean"),
            points_per_match=("points", "mean"),
            avg_shot_accuracy=("shot_accuracy", "mean"),
            matches=("team_name", "size"),
        )
    )
    benchmark = benchmark[benchmark["matches"] >= 30].copy()
    benchmark["highlight"] = benchmark["team_name"].eq("FC Barcelona")

    fig = px.scatter(
        benchmark,
        x="avg_possession",
        y="goals_per_match",
        size="points_per_match",
        color="league_name",
        text="team_name",
        hover_data=["avg_shot_accuracy", "matches"],
        title="Barcelona among selected European heavyweights",
    )
    fig.update_traces(
        textposition="top center",
        marker=dict(line=dict(width=1, color="white"), opacity=0.85),
    )
    barca_mask = benchmark["team_name"] == "FC Barcelona"
    fig.add_trace(
        go.Scatter(
            x=benchmark.loc[barca_mask, "avg_possession"],
            y=benchmark.loc[barca_mask, "goals_per_match"],
            mode="markers+text",
            text=benchmark.loc[barca_mask, "team_name"],
            textposition="bottom center",
            marker=dict(size=28, color="#912f40", symbol="diamond", line=dict(width=2, color="#ffffff")),
            name="Barcelona highlight",
            hovertemplate="FC Barcelona<br>Avg possession=%{x:.2f}<br>Goals per match=%{y:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        xaxis_title="Average possession (%)",
        yaxis_title="Goals per match",
        legend_title="League",
    )
    write_chart(fig, "act4_european_benchmark.html")


def main() -> None:
    master, barca = load_datasets()
    build_act1(barca)
    build_act2(barca)
    build_act3(barca)
    build_act4(master)
    print(f"Saved charts to {CHARTS}")


if __name__ == "__main__":
    main()
