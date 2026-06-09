import json


def serializeCourted(balconies, courted):
    serialized = {"balconies": {}, "matches": {}}
    for courtedId, suitors in balconies.items():
        serialized["balconies"][courtedId] = [suitor["id"] for suitor in suitors]
    for courtedEntity in courted:
        serialized["matches"][courtedEntity["id"]] = [
            suitor["id"] for suitor in courtedEntity["matches"]
        ]
    return serialized


def serializeSuitors(suitors):
    serialized = {"matches": {}}
    for suitor in suitors:
        serialized["matches"][suitor["id"]] = [
            match["id"] for match in suitor["matches"]
        ]
    return serialized


def serializeUnsuccessful(suitors, courted):
    unmatched = [
        {"id": s["id"], "filled": len(s["matches"]), "capacity": s["capacity"]}
        for s in suitors
        if len(s["matches"]) == 0
    ]
    vacant = [
        {"id": c["id"], "filled": len(c["matches"]), "capacity": c["capacity"]}
        for c in courted
        if len(c["matches"]) < c["capacity"]
    ]
    return {"suitors_with_no_match": unmatched, "courted_with_no_match": vacant}


def saveJSON(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
