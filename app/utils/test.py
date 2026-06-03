import subprocess

from app.matching.matchingLauncher import *
from app.visualization.textUI import *


def main() :
    generateDataSets()
    launchGUI()
    typeSuitors = determineSuitors()
    nbRounds =startMatching(typeSuitors)
    endMatching(nbRounds)

def generateDataSets():
    subprocess.run(
        ["python3", "./app/data/generate_datasets.py"],
        check=True
    )


if __name__ == "__main__" :
    main()
