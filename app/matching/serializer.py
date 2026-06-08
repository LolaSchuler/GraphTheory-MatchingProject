import json


def serializeCourted(roundNumber, balconies, courted):
    serialized = {"round": roundNumber, "balconies": {}, "matches": {}}
    for courtedId, suitors in balconies.items():
        serialized["balconies"][courtedId] = [suitor["id"] for suitor in suitors]
    for courtedEntity in courted:
        serialized["matches"][courtedEntity["id"]] = [
            suitor["id"] for suitor in courtedEntity["matches"]
        ]
    return serialized


def serializeSuitors(roundNumber, suitors):
    serialized = {"round": roundNumber, "matches": {}}
    for suitor in suitors:
        serialized["matches"][suitor["id"]] = [
            match["id"] for match in suitor["matches"]
        ]
    return serialized


def saveJSON(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
