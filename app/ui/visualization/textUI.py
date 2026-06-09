from app.matching.matchingLauncher import TYPE


def introGUI():
    print("\n         -------------------------------------------------\n")
    print("         -              Graph Theory Project             -\n")
    print("         -------------------------------------------------\n")
    print("               SCHÜLER Lola   -   WINTERHOFF Ophélie      \n\n")


def determineSuitors():
    while True:
        choice = input(
            "Tapez 0 si ce sont les écoles qui courtisent. Tapez 1 si ce sont les élèves.\n"
        )
        if choice == "0":
            return TYPE.SCHOOL
        elif choice == "1":
            return TYPE.STUDENTS


def endMatching(nbRounds):
    print("\nMatching fini\n")
    print(
        "Nombre de Rounds nécessaires pour trouver les meilleurs matchs : ",
        nbRounds,
        "\n",
    )
