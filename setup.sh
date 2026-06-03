#!/bin/bash
set -e

echo "Création de l'environnement virtuel..."
python3 -m venv .venv

echo "Activation de l'environnement..."
source .venv/bin/activate

echo "Mise à jour de pip..."
python -m pip install --upgrade pip

echo "Installation des dépendances..."
pip install -r ./requirements.txt

echo "Installation terminée."
