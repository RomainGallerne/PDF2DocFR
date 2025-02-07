@echo off
echo Vérification de Python...
where python >nul 2>nul || (
    echo Python n'est pas installé. Veuillez l'installer manuellement depuis https://www.python.org/downloads/
    exit /b
)

echo Création de l'environnement virtuel...
python -m venv .venv
call .venv\Scripts\activate

echo Installation des dépendances...
pip install --upgrade pip
pip install -r requirements.txt

echo Lancement de l'application...
python src.py
