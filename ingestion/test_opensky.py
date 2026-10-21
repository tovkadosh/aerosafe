"""Test rapide de l'API OpenSky Network.

Sans identifiants : accès anonyme (limité en quota).
Avec OPENSKY_CLIENT_ID / OPENSKY_CLIENT_SECRET dans .env : accès OAuth2.
"""
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://opensky-network.org/api/states/all"
TOKEN_URL = (
    "https://auth.opensky-network.org/auth/realms/opensky-network"
    "/protocol/openid-connect/token"
)

# Zone de test : France métropolitaine
BBOX = {"lamin": 41.3, "lomin": -5.2, "lamax": 51.1, "lomax": 9.6}


def get_token():
    client_id = os.getenv("OPENSKY_CLIENT_ID")
    client_secret = os.getenv("OPENSKY_CLIENT_SECRET")
    if not (client_id and client_secret):
        return None
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    print(f"Mode : {'authentifié' if token else 'anonyme'}")

    resp = requests.get(API_URL, params=BBOX, headers=headers, timeout=30)
    print(f"HTTP {resp.status_code}")
    remaining = resp.headers.get("X-Rate-Limit-Remaining")
    if remaining:
        print(f"Crédits restants : {remaining}")
    if resp.status_code != 200:
        print(resp.text[:500])
        sys.exit(1)

    data = resp.json()
    states = data.get("states") or []
    print(f"Horodatage : {data.get('time')} — {len(states)} avions dans la zone\n")

    # Champs : 0 icao24, 1 callsign, 2 pays, 5 lon, 6 lat, 7 alt baro (m), 9 vitesse (m/s)
    for s in states[:10]:
        callsign = (s[1] or "").strip() or "—"
        alt = f"{s[7]:.0f} m" if s[7] is not None else "sol/NA"
        speed = f"{s[9] * 3.6:.0f} km/h" if s[9] is not None else "NA"
        print(f"{s[0]}  {callsign:<8}  {s[2]:<15}  lat={s[6]}  lon={s[5]}  alt={alt}  v={speed}")


if __name__ == "__main__":
    main()
