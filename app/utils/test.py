import subprocess

from app.matching.matchingLauncher import startMatching
from app.visualization.textUI import introGUI, determineSuitors, endMatching


def main():
    introGUI()
    generateDataSets()
    typeSuitors = determineSuitors()
    nbRounds = startMatching(typeSuitors)
    endMatching(nbRounds)


def generateDataSets():
    subprocess.run(["python3", "./app/data/generate_datasets.py"], check=True)


if __name__ == "__main__":
    main()
