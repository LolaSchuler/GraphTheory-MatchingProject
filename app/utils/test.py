import subprocess

from app.matching.matchingLauncher import startMatching
from app.ui.visualization.textUI import launchGUI, determineSuitors, endMatching


def main():
    generateDataSets()
    launchGUI()
    typeSuitors = determineSuitors()
    nbRounds = startMatching(typeSuitors)
    endMatching(nbRounds)


def generateDataSets():
    subprocess.run(["python3", "./app/data/generate_datasets.py"], check=True)


if __name__ == "__main__":
    main()
