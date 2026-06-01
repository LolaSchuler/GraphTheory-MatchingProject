import json

from services.roundManager import *
from enum import Enum

class TYPE(Enum):
    SCHOOL, STUDENTS = range(2)

def startMatching(suitor):
    finished = False
    # Initialize suitors and courted
    if suitor == TYPE.SCHOOL :
        suitors = json.loads("./schools.json")
        courted = json.loads("./students.json")
    elif suitor == TYPE.STUDENTS :
        suitors = json.loads("./students.json")
        courted = json.loads("./schools.json")
    # Launch the matching loop
    while not finished :
        balconies = setupRound(suitors, courted)
        launchRound(balconies, suitors, courted)
        endRound(finished)
    endMatching()

def endMatching():
    pass