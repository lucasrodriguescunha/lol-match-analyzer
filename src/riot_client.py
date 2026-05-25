import os
import requests
from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
REGIONAL_HOST = "https://americas.api.riotgames.com"
QUEUE_RANKED_SOLO = 420


def get_last_ranked_match(riot_id: str) -> tuple[dict, str]:
    """
    Retorna (match_json, puuid) da partida ranqueada solo/duo mais recente.

    Args:
        riot_id: Identificador no formato 'GameName#TAG' (ex: 'Faker#KR1').

    Returns:
        Tupla (match, puuid) onde match é o JSON bruto da Match v5 e puuid
        é o identificador único do jogador, necessário para os extractors.
    """
    headers = {"X-Riot-Token": RIOT_API_KEY}

    game_name, tag_line = riot_id.split("#")

    account = requests.get(
        f"{REGIONAL_HOST}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
        headers=headers,
        timeout=10,
    ).json()

    if "puuid" not in account:
        status = account.get("status", {})
        raise RuntimeError(
            f"Riot API error {status.get('status_code')}: {status.get('message', account)}"
        )
    puuid = account["puuid"]

    match_ids = requests.get(
        f"{REGIONAL_HOST}/lol/match/v5/matches/by-puuid/{puuid}/ids",
        headers=headers,
        params={"queue": QUEUE_RANKED_SOLO, "count": 1},
        timeout=10,
    ).json()

    match = requests.get(
        f"{REGIONAL_HOST}/lol/match/v5/matches/{match_ids[0]}",
        headers=headers,
        timeout=10,
    ).json()

    return match, puuid


def get_match_timeline(match_id: str) -> dict:
    """
    Retorna o JSON da timeline da partida (eventos frame a frame).

    Args:
        match_id: ID da partida no formato 'BR1_XXXXXXXXX'.

    Returns:
        Dicionário com frames e eventos retornado pela API Match v5 da Riot.
    """
    headers = {"X-Riot-Token": RIOT_API_KEY}
    return requests.get(
        f"{REGIONAL_HOST}/lol/match/v5/matches/{match_id}/timeline",
        headers=headers,
        timeout=10,
    ).json()
