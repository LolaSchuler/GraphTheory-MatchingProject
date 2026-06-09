import streamlit as st

from app.matching.matchingLauncher import startMatching, TYPE, generateNewDatasets

st.set_page_config(page_title="Stable Parcoursup", layout="wide")

st.title("Stable Parcoursup")

st.checkbox("Show the matching process step by step", key="show_matching_process")

if st.button("Generate new datasets"):
    generateNewDatasets()
    st.success("New datasets generated")

st.radio(
    "Who are the suitors ?",
    ("Schools", "Students"),
    key="suitor_choice",
)

suitorChoice = (
    TYPE.SCHOOL if st.session_state.suitor_choice == "Schools" else TYPE.STUDENTS
)

if st.button("Start the matching process"):
    nbRounds = startMatching(suitorChoice)
    st.success(f"Matching finished in {nbRounds} rounds")
