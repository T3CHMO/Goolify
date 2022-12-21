import os

from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv

# Load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("score_db")


def insert_score(team_a, team_b, score_a, score_b, date):
    """Returns the match on a successful match creation, otherwise raises and error"""
    return db.put({"team_a": team_a, "team_b": team_b, "score_a": score_a, "score_b": score_b, "approved": "false", "date": date})


def fetch_all_matches():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items


def approve_match(key):
    return db.update({"approved": "true"}, key)

