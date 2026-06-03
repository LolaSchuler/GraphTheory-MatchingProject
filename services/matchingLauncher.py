import json

from services.roundManager import *
from enum import Enum

class TYPE(Enum):
    SCHOOL, STUDENTS = range(2)

def startMatching(suitor):
    schoolDataPath = "./schools.json"
    studentDataPath = "./students.json"
    # Initialize suitors and courted
    if suitor == TYPE.SCHOOL :
        suitors = json.loads(schoolDataPath)
        courted = json.loads(studentDataPath)
    elif suitor == TYPE.STUDENTS :
        suitors = json.loads(studentDataPath)
        courted = json.loads(schoolDataPath)
    # Launch the matching loop
    nbRounds = 0
    finished = False
    while not finished :
        nbRounds += 1
        balconies = setupRound(suitors, courted)
        launchRound(balconies, courted)
        finished = endRound(balconies, courted)
    return nbRounds

