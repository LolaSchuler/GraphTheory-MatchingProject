import json
import subprocess
from pathlib import Path
from enum import Enum
from app.matching.roundManager import setupRound, launchRound, endRound
from app.matching.serializer import (
    serializeCourted,
    saveJSON,
    serializeSuitors,
    serializeUnsuccessful,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "app" / "data" / "dataset"
OUTPUT_FILE_PATH = PROJECT_ROOT / "app" / "outputs" / "matching_output.json"
UNSUCCESSFUL_FILE_PATH = PROJECT_ROOT / "app" / "outputs" / "unsuccessful_entities.json"
ROUNDS_PATH = PROJECT_ROOT / "app" / "outputs" / "rounds"


class TYPE(Enum):
    SCHOOL, STUDENTS = range(2)


def startMatching(suitorChoice):
    # Initialize suitors and courted
    suitors, courted = initMatching(suitorChoice)
    # Launch the matching loop
    nbRounds = 0
    finished = False
    while not finished:
        nbRounds += 1
        balconies = setupRound(suitors, courted)
        launchRound(balconies, courted)
        finished = endRound(suitors)
        if not finished:
            data_suitors = serializeSuitors(suitors)
            data_courted = serializeCourted(balconies, courted)
            round_data = {
                "round": nbRounds,
                "suitors": data_suitors,
                "courted": data_courted,
            }
            saveJSON(round_data, str(ROUNDS_PATH / f"round_{nbRounds}.json"))
    final_matches = serializeSuitors(suitors)
    saveJSON(final_matches, OUTPUT_FILE_PATH)
    unmatched_and_vacant = serializeUnsuccessful(suitors, courted)
    saveJSON(unmatched_and_vacant, UNSUCCESSFUL_FILE_PATH)
    return nbRounds


def initMatching(suitorChoice):
    # Make sure every directory we are gonna use exists
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    UNSUCCESSFUL_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ROUNDS_PATH.mkdir(parents=True, exist_ok=True)
    # Clear content of rounds directory
    clearRoundsDirectory()

    # Load school and student data from json files
    schoolsDataPath = DATA_PATH / "schools.json"
    studentsDataPath = DATA_PATH / "students.json"
    # Initialize suitors and courted
    with open(schoolsDataPath, "r") as schoolsData:
        schools = json.loads(schoolsData.read())
    with open(studentsDataPath, "r") as studentsData:
        students = json.loads(studentsData.read())
    if suitorChoice == TYPE.SCHOOL:
        suitors = schools
        courted = students
    elif suitorChoice == TYPE.STUDENTS:
        suitors = students
        courted = schools
    # Add matches and current_wish fields to all entities
    for entity in schools + students:
        entity["matches"] = []
        entity["current_wish"] = 0
    return suitors, courted


def generateNewDatasets(nbSchools, nbStudents):
    subprocess.run(
        ["python3", "./app/data/generate_datasets.py", str(nbSchools), str(nbStudents)],
        check=True,
    )


def clearRoundsDirectory():
    for file in ROUNDS_PATH.glob("*.json"):
        file.unlink()
