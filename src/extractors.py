def _find_participant(match: dict, puuid: str) -> dict:
    for p in match["info"]["participants"]:
        if p["puuid"] == puuid:
            return p
    raise ValueError(f"PUUID {puuid} not found in match participants")


def extract_kda(match: dict, puuid: str) -> dict:
    """Retorna kills, deaths, assists e KDA ratio do jogador na partida."""
    p = _find_participant(match, puuid)
    k, d, a = p["kills"], p["deaths"], p["assists"]
    return {
        "kills": k,
        "deaths": d,
        "assists": a,
        "kda_ratio": round((k + a) / max(d, 1), 2),
    }


def extract_death_timeline(match: dict, timeline: dict, puuid: str) -> list[dict]:
    """Retorna lista de mortes com timestamp (min) e posição no mapa."""
    participants = match["info"]["participants"]
    participant_id = next(
        i + 1 for i, p in enumerate(participants) if p["puuid"] == puuid
    )

    deaths = []
    for frame in timeline["info"]["frames"]:
        for event in frame["events"]:
            if event.get("type") == "CHAMPION_KILL" and event.get("victimId") == participant_id:
                deaths.append({
                    "timestamp_ms": event["timestamp"],
                    "timestamp_min": round(event["timestamp"] / 60000, 1),
                    "position": event.get("position", {}),
                    "killer_id": event.get("killerId", 0),
                })
    return deaths


def extract_lane_matchup(match: dict, puuid: str) -> dict:
    """Retorna campeão do jogador, posição e campeão oponente na lane."""
    p = _find_participant(match, puuid)
    position = p.get("teamPosition", "UNKNOWN")
    champion = p["championName"]
    team_id = p["teamId"]

    opponents = [
        x for x in match["info"]["participants"]
        if x.get("teamPosition") == position and x["teamId"] != team_id
    ]
    opponent = opponents[0]["championName"] if opponents else "Unknown"

    return {
        "champion": champion,
        "position": position,
        "opponent_champion": opponent,
    }
