import json
from pathlib import Path
from app.matching.roundManager import setupRound, launchRound, endRound
from enum import Enum

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "app" / "data" / "dataset"
OUTPUT_PATH = PROJECT_ROOT / "app" / "outputs" / "matching_output.json"

DATA_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


class TYPE(Enum):
    SCHOOL, STUDENTS = range(2)


def initMatching(suitorChoice):
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
    createOutputJSON(suitors, courted)
    return nbRounds


def createOutputJSON(suitors, courted):
    output = []
    for suitor in suitors:
        for match in suitor["matches"]:
            courtedEntity = next((c for c in courted if c["id"] == match["id"]), None)
            if courtedEntity is not None:
                output.append(
                    {
                        "suitor_id": suitor["id"],
                        "suitor_name": suitor.get("name", suitor["id"]),
                        "courted_id": courtedEntity["id"],
                        "courted_name": courtedEntity.get("name", courtedEntity["id"]),
                    }
                )
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
