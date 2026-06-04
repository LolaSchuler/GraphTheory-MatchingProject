import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

DATASET_DIR.mkdir(exist_ok=True)

NUM_SCHOOLS = 3
NUM_STUDENTS = NUM_SCHOOLS * 15

academies = ["Versailles", "Toulouse", "Paris", "Lyon"]
school_types = ["BTS", "Université", "IUT", "CPGE"]

# Capacity
weights = [random.uniform(0.5, 1.5) for i in range(NUM_SCHOOLS)]
weight_sum = sum(weights)

capacities = [int(NUM_STUDENTS * w / weight_sum) for w in weights]

diff = NUM_STUDENTS - sum(capacities)

i = 0
while diff != 0:
    if diff > 0:
        capacities[i] += 1
        diff -= 1
    else:
        if capacities[i] > 1:
            capacities[i] -= 1
            diff += 1
    i = (i + 1) % NUM_SCHOOLS

# School Generation
schools = []

for i in range(NUM_SCHOOLS):
    school_id = f"S{i + 1}"

    school_type = random.choice(school_types)

    capacity = capacities[i]

    quotas = {
        "BTS": {
            "general": int(capacity * 0.5),
            "technological": int(capacity * 0.3),
            "professional": capacity - int(capacity * 0.5) - int(capacity * 0.3),
        },
        "Université": {
            "general": int(capacity * 0.6),
            "technological": int(capacity * 0.2),
            "professional": capacity - int(capacity * 0.6) - int(capacity * 0.2),
        },
        "IUT": {
            "general": int(capacity * 0.4),
            "technological": int(capacity * 0.4),
            "professional": capacity - int(capacity * 0.4) - int(capacity * 0.4),
        },
        "CPGE": {
            "general": int(capacity * 0.8),
            "technological": int(capacity * 0.2),
            "professional": capacity - int(capacity * 0.8) - int(capacity * 0.1),
        },
    }[school_type]

    minimum_grade = {"BTS": 9, "Université": 10, "IUT": 12, "CPGE": 15}[school_type]

    specialty_bonus = {
        "BTS": {"general": 0, "technological": 1, "professional": 2},
        "Université": {"general": 2, "technological": 1, "professional": 1},
        "IUT": {"general": 1, "technological": 2, "professional": 0},
        "CPGE": {"general": 3, "technological": 0, "professional": 0},
    }[school_type]

    selection = {
        "academy_bonus": random.choice([0, 1, 2, 3]),
        "minimum_grade": minimum_grade,
        "specialty_bonus": specialty_bonus,
    }

    schools.append(
        {
            "id": school_id,
            "name": f"School {school_id}",
            "academy": random.choice(academies),
            "type": school_type,
            "capacity": capacity,
            "quotas": quotas,
            "selection": selection,
            "wishes": [],
        }
    )

# Student Generation
students = []

for i in range(1, NUM_STUDENTS + 1):
    if i <= NUM_STUDENTS * 0.5:
        specialty = "general"
    elif i <= NUM_STUDENTS * 0.75:
        specialty = "technological"
    else:
        specialty = "professional"

    student_wishes = random.sample([school["id"] for school in schools], k=NUM_SCHOOLS)
    grade = round(random.uniform(9, 20), 1)

    students.append(
        {
            "id": f"E{i:03}",
            "specialty": specialty,
            "grade": grade,
            "academy": random.choice(academies),
            "capacity": 1,
            "wishes": [
                {"id": school, "rank": rank + 1}
                for rank, school in enumerate(student_wishes)
            ],
        }
    )

# Rewrite schools wishes
for school in schools:
    school_wishes = random.sample(
        [student["id"] for student in students], k=NUM_STUDENTS
    )
    school["wishes"] = [
        {"id": student, "rank": rank + 1} for rank, student in enumerate(school_wishes)
    ]

# Export
with open(DATASET_DIR / "schools.json", "w", encoding="utf-8") as f:
    json.dump(schools, f, indent=4)

with open(DATASET_DIR / "students.json", "w", encoding="utf-8") as f:
    json.dump(students, f, indent=4)

print("Generation Successful")
