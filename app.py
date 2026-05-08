import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="NFL Player Performance Tracker",
    page_icon="🏈",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/nfl_player_stats.csv")

df = load_data()

st.title("🏈 NFL Player Performance Tracker")
st.write(
    "Track NFL player performance by position, team, and season. "
    "This dashboard is built with Python, Pandas, Streamlit, and Plotly."
)

with st.sidebar:
    st.header("Filters")
    player_search = st.text_input("Search player")
    positions = st.multiselect(
        "Position",
        sorted(df["position"].unique()),
        default=sorted(df["position"].unique())
    )
    teams = st.multiselect(
        "Team",
        sorted(df["team"].unique()),
        default=sorted(df["team"].unique())
    )

filtered = df[
    df["position"].isin(positions) &
    df["team"].isin(teams)
]

if player_search:
    filtered = filtered[
        filtered["player"].str.contains(player_search, case=False, na=False)
    ]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Players", len(filtered))
col2.metric("Total Passing Yards", int(filtered["passing_yards"].sum()))
col3.metric("Total Rushing Yards", int(filtered["rushing_yards"].sum()))
col4.metric("Avg Fantasy Points", round(filtered["fantasy_points_est"].mean(), 1) if len(filtered) else 0)

st.subheader("Player Stats")
st.dataframe(filtered, use_container_width=True)

st.subheader("Top Players by Estimated Fantasy Points")
top_players = filtered.sort_values("fantasy_points_est", ascending=False).head(10)

fig = px.bar(
    top_players,
    x="player",
    y="fantasy_points_est",
    color="position",
    title="Estimated Fantasy Points by Player"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Passing Yards vs Rushing Yards")
scatter = px.scatter(
    filtered,
    x="passing_yards",
    y="rushing_yards",
    color="position",
    hover_name="player",
    size="fantasy_points_est",
    title="Player Performance Comparison"
)
st.plotly_chart(scatter, use_container_width=True)

st.subheader("Simple Player Comparison")
selected_players = st.multiselect(
    "Choose players to compare",
    filtered["player"].unique()
)

if selected_players:
    comparison = filtered[filtered["player"].isin(selected_players)]
    st.dataframe(comparison, use_container_width=True)

    compare_fig = px.bar(
        comparison,
        x="player",
        y=["passing_yards", "rushing_yards", "fantasy_points_est"],
        barmode="group",
        title="Player Comparison"
    )
    st.plotly_chart(compare_fig, use_container_width=True)
else:
    st.info("Select players above to compare their performance.")
