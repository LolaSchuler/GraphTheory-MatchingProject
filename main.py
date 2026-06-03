from services.matchingLauncher import *
from ui.mainWindow import *


def main() :
    launchGUI()
    typeSuitors = determineSuitors()
    nbRounds =startMatching(typeSuitors)
    endMatching(nbRounds)
    


if __name__ == "__main__" :
    main()
