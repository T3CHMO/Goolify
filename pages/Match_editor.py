import streamlit as st
import streamlit_authenticator as stauth
from datetime import date

from database import users_db as db
from database import score_db as score_db

st.title('Match editor')
# Allow custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# AUTHENTICATION

users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
passwords = [user["password"] for user in users]

credentials = {"usernames": {}}
for uname, name, pwd in zip(usernames, names, passwords):
    user_dict = {"name": name, "password": pwd}
    credentials["usernames"].update({uname: user_dict})

authenticator = stauth.Authenticate(credentials, "goolify_dashboard", "secret", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # After successful login edit page is accessible
    st.caption('You are logged in as {}.'.format(username))
    authenticator.logout("Logout", "sidebar")
    # Data preparation, filtering
    teams = [key["key"] for key in db.fetch_all_users()]
    # Filter other teams then my
    other_teams = [team for team in teams if team != username]
    matches = score_db.fetch_all_matches()
    # Filter not approved matches
    not_approved_matches = [a for a in matches if a['approved'] == "false" and a['team_b'] == username]

    st.header("Add match")


    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.text("Your Team:")
        col1.markdown(username)
        selected_team_a = username
        selected_score_a = col1.number_input("Score:", min_value=0, format="%i", step=1, key="score_a")
        selected_team_b = col2.selectbox("Select Team:", other_teams, key="team_b", index=0)
        selected_score_b = col2.number_input("Score:", min_value=0, format="%i", step=1, key="score_b")
        match_date = st.date_input(
            "When did you played the match?",
            date.today())
        st.write('Match was played on :', match_date)

        if selected_team_a == selected_team_b:
            st.error("Select different team!")

        submitted = st.form_submit_button("Add match")
        if submitted:
            score_db.insert_score(selected_team_a, selected_team_b, selected_score_a, selected_score_b, str(match_date))
            st.success("Match saved!")

    st.header("Approve match")
    with st.form("approve_form", clear_on_submit=True):
        key = st.selectbox("Approve Match:", not_approved_matches, key="matches", index=0, format_func=lambda x: str(x['team_a'] + ' '+ str(x['score_a']) + ' : ' + str(x['score_b']) + ' ' + x['team_b']))

        submitted = st.form_submit_button("Approve")
        if submitted:
            score_db.approve_match(key['key'])
            st.success("Approved!")
