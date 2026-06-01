
from services.matchingLauncher import TYPE

def launchGUI() :
    print("-------------------------------------------------\n")
    print("-              Graph Theory Project             -\n")
    print("-------------------------------------------------\n")

def determineSuitors():
    choice = input("Tapez 0 si ce sont les écoles qui courtisent. Tapez 1 si ce sont les élèves.\n")
    if choice == 0 :
        return TYPE.SCHOOL
    elif choice == 1 :
        return TYPE.STUDENTS

def endMatching(nbRounds):
    print("\nMatching fini\n")
    print("Nombre de Rounds nécessaires pour que tous les élèves aient une place : ", nbRounds)
    