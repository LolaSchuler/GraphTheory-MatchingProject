

def setupRound(suitors, courted) :
    # Every suitor goes to its favorite's balcony
    balconies = []
    # Initialize empty balconies for every courted
    for i in range(len(courted)) :
        balconies[i] = []
    # Loops through suitors to make each one go to the right balcony
    for suitor in suitors :
        suitorWishes = suitor["wishes"]
        # Find the right courted according to the current wish
        currentWishName = suitorWishes[suitor["current_wish"]]["name"]
        balconyNumber = getIndexInWishesByName(courted, currentWishName)
        # Add the suitor's name to the right courted's balcony
        balconies[balconyNumber].append(suitor)
    return balconies

def launchRound(balconies, courted) :
    # Each courted chooses its preferred suitor
    for i in range(len(courted)) :
        # If the courted has less than two suitors, it doesn't have to choose
        if len(balconies[i]) < 2 :
            continue
        # If the courted has 2 or more suitors, it has to choose its favorite
        preferredSuitorName = balconies[i][0]["name"]
        for suitor in balconies[i] :
            if prefers(courted[i], preferredSuitorName, suitor["name"]) :
                preferredSuitorName = suitor["name"]
                suitor["current_wish"] -= 1


def endRound(balconies, courted) :
    # Verify if everyone is paired up
    for i in range(len(courted)) :
        if len(balconies[i]) != 1 :
            return False
    return True

def prefers(courted, suitor1Name, suitor2Name) :
    # Returns True if the courted one prefers suitor1 to suitor2. Else, returns False.
    wishes = courted["wishes"]
    rankSuitor1 = getRankByName(wishes, suitor1Name)
    rankSuitor2 = getRankByName(wishes, suitor2Name)
    if rankSuitor1 > rankSuitor2 :
        return True
    else :
        return False


def getRankByName(wishes, name) :
    # Parse through the wishes and returns the rank of the wish corresponding to the name
    for i in range(len(wishes)) :
        if wishes[i]["name"] == name :
            return wishes[i]["rank"]

def getIndexInWishesByName(wishes, name) :
    # Parse through the wishes and returns the index of the wish corresponding to the name
    for j in range(len(wishes)) :
        if name == wishes[j]["name"] :
            return j

