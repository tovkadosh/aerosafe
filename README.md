# AeroSafe

Projet de génie logiciel (IPSA) — ingestion et analyse de données aériennes via l'API OpenSky Network.

## Installation

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
pip install -r requirements.txt
```

Copier vos identifiants OpenSky (optionnels) dans un fichier `.env` :

```
OPENSKY_CLIENT_ID=...
OPENSKY_CLIENT_SECRET=...
```

## Test rapide

```bash
python ingestion/test_opensky.py
```
