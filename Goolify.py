import streamlit as st
from database import score_db as score_db


st.set_page_config(page_title="Goolify ⚽")
st.title('Goolify ⚽')


st.caption('This is an application to track football scores.')
st.header('Latest games')

matches = score_db.fetch_all_matches()
team_as = [team_a["team_a"] for team_a in matches]
team_bs = [team_b["team_b"] for team_b in matches]
score_as = [score_a["score_a"] for score_a in matches]
score_bs = [score_b["score_b"] for score_b in matches]

for idx, x in enumerate(matches):
    st.subheader(team_as[idx] + ' ' + str(score_as[idx]) + ':' + str(score_bs[idx]) + ' ' + team_bs[idx])




