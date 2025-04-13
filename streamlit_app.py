import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="MLB Prediction Dashboard", layout="wide")
st.title("MLB Prediction Dashboard")

# Tabs
moneyline_tab, runline_tab, totals_tab, props_tab, odds_tab, research_tab, ai_tab = st.tabs([
    "Moneyline", "Run Line (Spreads)", "Totals (Over/Under)", "Player Props", "Odds & Edge Finder", "Team/Player Research", "AI Prompter"])

# --- Moneyline Tab ---
with moneyline_tab:
    st.header("Today's Moneyline Predictions")
    try:
        with open("mlb_today_predictions.json") as f:
            ml_data = json.load(f)
        ml_df = pd.DataFrame(ml_data)
        st.dataframe(ml_df)
    except Exception as e:
        st.warning(f"Moneyline predictions not available: {e}")

# --- Run Line (Spreads) Tab ---
with runline_tab:
    st.header("Run Line Predictions")
    try:
        uploaded_spread = st.file_uploader("Upload mlb_spread_predictions.json", type="json")
        if uploaded_spread:
            spread_data = json.load(uploaded_spread)
            spread_df = pd.DataFrame(spread_data)
            st.dataframe(spread_df)
    except Exception as e:
        st.warning(f"No run line predictions available: {e}")

# --- Totals Tab ---
with totals_tab:
    st.header("Over/Under Predictions")
    try:
        uploaded_totals = st.file_uploader("Upload mlb_totals_predictions.json", type="json")
        if uploaded_totals:
            totals_data = json.load(uploaded_totals)
            totals_df = pd.DataFrame(totals_data)
            st.dataframe(totals_df)
    except Exception as e:
        st.warning(f"No totals predictions available: {e}")

# --- Player Props Tab ---
with props_tab:
    st.header("Player Prop Predictions")
    try:
        uploaded_props = st.file_uploader("Upload mlb_props_predictions.json", type="json")
        if uploaded_props:
            props_data = json.load(uploaded_props)
            props_df = pd.DataFrame(props_data)
            st.dataframe(props_df)
    except Exception as e:
        st.warning(f"No player props available: {e}")

# --- Odds & Edge Finder Tab ---
with odds_tab:
    st.header("Odds Comparison & Value Bets")
    try:
        uploaded_odds = st.file_uploader("Upload today_odds.csv", type="csv")
        uploaded_preds = st.file_uploader("Upload mlb_today_predictions.json (for model probs)", type="json")

        if uploaded_odds and uploaded_preds:
            odds_df = pd.read_csv(uploaded_odds)
            preds = json.load(uploaded_preds)
            preds_df = pd.DataFrame(preds)

            def implied_prob(odds):
                return 100 / (odds + 100) if odds > 0 else -odds / (-odds + 100)

            odds_df['team'] = odds_df['team'].astype(str)
            odds_df['ml_implied_prob'] = odds_df['ml_odds'].apply(implied_prob)

            merged = pd.merge(odds_df, preds_df, on=['home_team', 'away_team', 'team'], how='inner')

            merged['model_prob'] = merged.apply(
                lambda row: row['home_win_prob'] if row['team'] == row['home_team'] else row['away_win_prob'], axis=1)

            merged['edge'] = (merged['model_prob'] - merged['ml_implied_prob']) * 100

            st.dataframe(merged[['home_team', 'away_team', 'team', 'ml_odds', 'ml_implied_prob', 'model_prob', 'edge']])
    except Exception as e:
        st.warning(f"Could not display edge detection: {e}")

# --- Research Tab ---
with research_tab:
    st.header("Team/Player Rolling Averages & Matchup Stats")
    st.info("This section will include filters and stats for any MLB team or player. Coming soon...")

# --- AI Prompter ---
with ai_tab:
    st.header("Ask AI Anything About MLB Stats")
    user_input = st.text_input("Ask a question or type a prompt")
    if user_input:
        st.write("(Response placeholder: AI output will be shown here.)")
