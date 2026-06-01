from services.matchingLauncher import *
from ui.GUI import *


def main() :
    launchGUI()
    typeSuitors = determineSuitors()
    startMatching(typeSuitors)
    


if __name__ == "main" :
    main()