import streamlit as st
import pandas as pd
import json

from app.matching.matchingLauncher import (
    startMatching,
    TYPE,
    generateNewDatasets,
    OUTPUT_FILE_PATH,
    UNSUCCESSFUL_FILE_PATH,
    ROUNDS_PATH,
    DATA_PATH,
)


def highlight_status(row):
    if "Accepté" in row["Statut"]:
        return ["", "", "background-color: #d4edda; color: #155724"]
    else:
        return ["", "", "background-color: #f8d7da; color: #721c24"]


st.set_page_config(page_title="Stable Parcoursup", layout="wide")
st.title("Stable Parcoursup")

# États de session
# Pour n'afficher les métriques qu'une fois qu'on a lancé le matching pour la première fois
if "matching_done" not in st.session_state:
    st.session_state.matching_done = False

if "current_round_index" not in st.session_state:
    st.session_state.current_round_index = 0

if "nb_rounds" not in st.session_state:
    st.session_state.nb_rounds = None

# Génération des datasets
col1, col2 = st.columns(2)
col1.number_input(
    "Number of schools",
    min_value=1,
    step=1,
    value=3,
    key="nb_schools",
)
col2.number_input(
    "Number of students",
    min_value=1,
    step=1,
    value=50,
    key="nb_students",
)

if st.button("Generate new datasets"):
    generateNewDatasets(
        nbSchools=st.session_state.nb_schools,
        nbStudents=st.session_state.nb_students,
    )
    # Invalidation des anciens résultats
    st.session_state.matching_done = False
    st.session_state.nb_rounds = None
    st.session_state.current_round_index = 0
    # Affichage utilisateur
    st.success("New datasets generated")

# Choix des suitors
st.radio(
    "Who are the suitors ?",
    ("Schools", "Students"),
    key="suitor_choice",
)
# Si on change de mode, on invalide le matching précédent
prev_choice = st.session_state.get("prev_suitor_choice", None)
if prev_choice is not None and prev_choice != st.session_state.suitor_choice:
    st.session_state.matching_done = False
    st.session_state.nb_rounds = None
    st.session_state.current_round_index = 0
st.session_state.prev_suitor_choice = st.session_state.suitor_choice

# Traduction du choix utilisateur des suitors
suitorChoice = (
    TYPE.SCHOOL if st.session_state.suitor_choice == "Schools" else TYPE.STUDENTS
)

# Invalidation si les paramètres changent après un matching
current_config = {
    "suitor": st.session_state.suitor_choice,
    "schools": st.session_state.nb_schools,
    "students": st.session_state.nb_students,
}
if (
    "last_matching_config" in st.session_state
    and current_config != st.session_state.last_matching_config
):
    st.session_state.matching_done = False

# Démarrage du matching
if st.button("Start the matching process"):
    nbRounds = startMatching(suitorChoice)

    st.session_state.nb_rounds = nbRounds
    st.session_state.matching_done = True
    st.session_state.current_round_index = 0
    st.session_state.last_matching_config = {
        "suitor": st.session_state.suitor_choice,
        "schools": st.session_state.nb_schools,
        "students": st.session_state.nb_students,
    }
    st.success(f"Matching finished in {nbRounds} rounds")


st.checkbox(
    "Show the matching process step by step",
    key="show_matching_process",
)


# Présentation des résultats
if st.session_state.matching_done:
    # Chargement matches réussis
    with open(OUTPUT_FILE_PATH) as f:
        raw_matches = json.load(f)["matches"]
    # Si c'est les étudiants les suitors, il faut inverser
    # les matches pour pouvoir présenter les résultats par école
    if suitorChoice == TYPE.STUDENTS:
        # Regroupement par école
        matches_by_school = {}
        for student_id, school_ids in raw_matches.items():
            for school_id in school_ids:
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
    # Si c'est les écoles les suitors, il faut inverser les matches ratés
    # pour pouvoir présenter les résultats ratés par étudiant
    else:
        unmatched_students = [e["id"] for e in unsuccessful["courted_with_no_match"]]
        vacant_schools = unsuccessful["suitors_with_no_match"]

    total_matched = sum(len(students) for students in matches_by_school.values())
    total_students = total_matched + len(unmatched_students)
    pct = round(total_matched / total_students * 100) if total_students > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Étudiants affectés", total_matched)
    col2.metric("Taux d'affectation", f"{pct}%")
    col3.metric("Étudiants non affectés", len(unmatched_students))
    col4.metric("Rounds", st.session_state.nb_rounds)

    # Chargement des données des étudiants et des écoles
    with open(DATA_PATH / "dataset" / "schools.json") as f:
        schools_data = {s["id"]: s for s in json.load(f)}
    with open(DATA_PATH / "dataset" / "students.json") as f:
        students_data = {s["id"]: s for s in json.load(f)}

    # Présenter les affectations par école
    st.subheader("Affectations par école")
    for school_id, student_ids in matches_by_school.items():
        school = schools_data.get(school_id, {})
        capacity = school.get("capacity", "?")
        school_type = school.get("type", "?")
        nb_matched = len(student_ids)

        with st.expander(
            f"{school_id} ({school_type}) — {nb_matched} / {capacity} étudiants"
        ):
            if student_ids:
                rows = []
                for sid in student_ids:
                    student = students_data.get(sid, {})
                    wish_rank = next(
                        (
                            w["rank"]
                            for w in student.get("wishes", [])
                            if w["id"] == school_id
                        ),
                        None,
                    )
                    rows.append(
                        {
                            "Étudiant": sid,
                            "Spécialité": student.get("specialty", "?"),
                            "Moyenne": student.get("grade", "?"),
                            "N° de vœu": str(wish_rank)
                            if wish_rank is not None
                            else "?",
                        }
                    )
                st.dataframe(
                    pd.DataFrame(rows),
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.caption("Aucun étudiant affecté.")

    # Présenter les étudiants non affectés à une école
    if unmatched_students:
        st.subheader("Non affectés")
        rows = []
        for sid in unmatched_students:
            student = students_data.get(sid, {})
            rows.append(
                {
                    "Étudiant": sid,
                    "Spécialité": student.get("specialty", "?"),
                    "Moyenne": student.get("grade", "?"),
                    "Vœux": ", ".join(w["id"] for w in student.get("wishes", [])),
                }
            )
        st.dataframe(
            pd.DataFrame(rows),
            width="stretch",
            hide_index=True,
        )
    else:
        st.success("Tous les étudiants ont été affectés.")

    # Présentation des rounds individuels
    if st.session_state.show_matching_process:
        st.subheader("Processus de matching")
        rounds_path = ROUNDS_PATH
        round_files = sorted(
            rounds_path.glob("round_*.json"), key=lambda f: int(f.stem.split("_")[1])
        )
        if not round_files:
            st.info("No round data available.")
            st.stop()

        total_rounds = len(round_files)

        # Au cas où le nombre de rounds change entre deux matchings
        if st.session_state.current_round_index >= total_rounds:
            st.session_state.current_round_index = 0

        # Navigation entre les rounds
        col_prev, col_label, col_next = st.columns([1, 3, 1])
        with col_prev:
            if st.button(
                "← Précédent", disabled=st.session_state.current_round_index == 0
            ):
                st.session_state.current_round_index -= 1
                st.rerun()
        with col_label:
            st.markdown(
                f"<div style='text-align:center; font-weight:bold; padding-top:6px;'>"
                f"Round {st.session_state.current_round_index + 1} / {total_rounds}</div>",
                unsafe_allow_html=True,
            )
        with col_next:
            if st.button(
                "Suivant →",
                disabled=st.session_state.current_round_index == total_rounds - 1,
            ):
                st.session_state.current_round_index += 1
                st.rerun()

        # Affichage du round actuel
        round_file = round_files[st.session_state.current_round_index]
        with open(round_file) as f:
            round_data = json.load(f)
        balconies = round_data["courted"]["balconies"]
        matches = round_data["courted"]["matches"]

        rows = []
        for courted_id, suitors_in_balcony in balconies.items():
            accepted = matches.get(courted_id, [])
            for suitor_id in suitors_in_balcony:
                status = "Accepté" if suitor_id in accepted else "Refusé"
                rows.append(
                    {
                        "Courtisé": courted_id,
                        "Courtisant": suitor_id,
                        "Statut": status,
                    }
                )
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(
                df.style.apply(highlight_status, axis=1),
                width="stretch",
                hide_index=True,
            )
        else:
            st.caption("Aucun candidat ce round.")
