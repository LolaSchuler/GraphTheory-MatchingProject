def setupRound(suitors, courted):
    balconies = {}
    for courtedEntity in courted:
        balconies[courtedEntity["id"]] = []
    for suitor in suitors:
        # If suitor's capacity is full for now
        if len(suitor["matches"]) == suitor["capacity"]:
            continue
        # If no more wishes for this suitor
        if suitor["current_wish"] >= len(suitor["wishes"]):
            continue
        # Else, add the suitor to his n first wishes' balconies, n being the suitor's capacity
        slots_available = suitor["capacity"] - len(suitor["matches"])
        while slots_available > 0 and suitor["current_wish"] < len(suitor["wishes"]):
            targetId = suitor["wishes"][suitor["current_wish"]]["id"]
            balconies[targetId].append(suitor)
            suitor["current_wish"] += 1
            slots_available -= 1
    return balconies


def launchRound(balconies, courted):
    for courtedEntity in courted:
        # Get the candidates for this courted entity (current matches + new suitors in the balcony)
        courtedId = courtedEntity["id"]
        candidates = courtedEntity["matches"] + balconies[courtedId]
        # Remove from the candidates all those who aren't in the courted's wishes
        candidates = [
            s
            for s in candidates
            if any(w["id"] == courtedId for w in s.get("wishes", []))
        ]
        # Sort the candidates according to the wishes of the courtedEntity
        wishes = courtedEntity["wishes"]
        candidates.sort(key=lambda suitor: getRankById(wishes, suitor["id"]))
        # Keep only the best candidates according to the capacity of the courted entity and reject all others
        accepted = candidates[: courtedEntity["capacity"]]
        rejected = candidates[courtedEntity["capacity"] :]
        # Update matches of courtedEntity and of accepted suitors
        courtedEntity["matches"] = accepted
        for acceptedSuitor in accepted:
            if courtedEntity not in acceptedSuitor["matches"]:
                acceptedSuitor["matches"].append(courtedEntity)
        # Update the rejected candidates by removing the match and moving on to the next wish
        for rejectedSuitor in rejected:
            if courtedEntity in rejectedSuitor["matches"]:
                rejectedSuitor["matches"].remove(courtedEntity)


def endRound(suitors):
    for suitor in suitors:
        # Suitor still has some space available
        if len(suitor["matches"]) < suitor["capacity"]:
            # Suitor still has some wishes available
            if suitor["current_wish"] < len(suitor["wishes"]):
                return False
    return True


def getRankById(wishes, suitorId):
    # Parse through the wishes and returns the rank of the wish corresponding to the id
    for i in range(len(wishes)):
        if wishes[i]["id"] == suitorId:
            return wishes[i]["rank"]
    return float("inf")
