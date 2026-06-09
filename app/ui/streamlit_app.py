import streamlit as st
import json

from app.matching.matchingLauncher import (
    startMatching,
    TYPE,
    generateNewDatasets,
    OUTPUT_FILE_PATH,
    UNSUCCESSFUL_FILE_PATH,
)

st.set_page_config(page_title="Stable Parcoursup", layout="wide")
st.title("Stable Parcoursup")

# Pour n'afficher les métriques qu'une fois qu'on a lancé le matching pour la première fois
if "matching_done" not in st.session_state:
    st.session_state.matching_done = False

# TODO : montrer le processus step by step !
st.checkbox("Show the matching process step by step", key="show_matching_process")

# Génération des datasets
st.number_input(
    label="Number of schools", min_value=1, step=1, value=3, key="nb_schools"
)
st.number_input(
    label="Number of students", min_value=1, step=1, value=50, key="nb_students"
)
if st.button("Generate new datasets"):
    generateNewDatasets(
        nbSchools=st.session_state.nb_schools,
        nbStudents=st.session_state.nb_students,
    )
    st.success("New datasets generated")

# Lancement du matching
st.radio("Who are the suitors ?", ("Schools", "Students"), key="suitor_choice")
suitorChoice = (
    TYPE.SCHOOL if st.session_state.suitor_choice == "Schools" else TYPE.STUDENTS
)
if st.button("Start the matching process"):
    nbRounds = startMatching(suitorChoice)
    st.session_state.nb_rounds = nbRounds
    st.success(f"Matching finished in {nbRounds} rounds")
    st.session_state.matching_done = True


# Présentation des résultats
if st.session_state.matching_done:
    # Chargement matches réussis
    with open(OUTPUT_FILE_PATH) as f:
        raw_matches = json.load(f)["matches"]
    # Si c'est les étudiants les suitors, il faut inverser les matches pour pouvoir présenter les résultats par école
    if suitorChoice == TYPE.STUDENTS:
        # Regroupement par école
        matches_by_school = {}
        for student_id, schools in raw_matches.items():
            for school_id in schools:
                matches_by_school.setdefault(school_id, []).append(student_id)
    else:
        # Déjà bon
        matches_by_school = raw_matches

    # Chargement matches ratés
    with open(UNSUCCESSFUL_FILE_PATH) as f:
        unsuccessful = json.load(f)
    if suitorChoice == TYPE.STUDENTS:
        # Déjà bon
        unmatched_students = [e["id"] for e in unsuccessful["suitors_with_no_match"]]
        vacant_schools = unsuccessful["courted_with_no_match"]
    # Si c'est les écoles les suitors, il faut inverser les matches ratés pour pouvoir présenter les résultats ratés par étudiant
    else:
        unmatched_students = [e["id"] for e in unsuccessful["courted_with_no_match"]]
        vacant_schools = unsuccessful["suitors_with_no_match"]

    total_matched = sum(len(v) for v in matches_by_school.values())

    col1, col2, col3 = st.columns(3)
    col1.metric("Étudiants affectés", total_matched)
    col2.metric("Étudiants non affectés", len(unmatched_students))
    col3.metric("Rounds", st.session_state.get("nb_rounds", "—"))

    # Présenter les affectations par école
    st.subheader("Affectations par école")
    for school, students in matches_by_school.items():
        with st.expander(f"{school} — {len(students)} étudiants"):
            st.write(", ".join(students))

    # Présenter les étudiants non affectés à une école

    # Non affectés
    if len(unmatched_students) > 0:
        st.subheader("Non affectés")
        st.warning(", ".join(unmatched_students))
    else:
        st.success("Tous les étudiants ont été affectés.")
