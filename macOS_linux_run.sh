#!/bin/bash

echo "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "Création de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Lancement de l'application..."
python3 src.py
