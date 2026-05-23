def _find_participant(match: dict, puuid: str) -> dict:
    """
    Localiza o participante pelo PUUID dentro do JSON da partida.

    Args:
        match: JSON bruto da partida (Match v5).
        puuid: PUUID do jogador.

    Returns:
        Dicionário do participante em match["info"]["participants"].

    Raises:
        ValueError: Se o PUUID não for encontrado na partida.
    """
    for p in match["info"]["participants"]:
        if p["puuid"] == puuid:
            return p
    raise ValueError(f"PUUID {puuid} not found in match participants")


def extract_kda(match: dict, puuid: str) -> dict:
    """
    Extrai KDA e ratio do jogador na partida.

    Args:
        match: JSON bruto da partida (Match v5).
        puuid: PUUID do jogador.

    Returns:
        Dicionário com kills, deaths, assists e kda_ratio.
        kda_ratio = (kills + assists) / max(deaths, 1).

    Example:
        >>> extract_kda(match, puuid)
        {"kills": 7, "deaths": 3, "assists": 5, "kda_ratio": 4.0}
    """
    p = _find_participant(match, puuid)
    k, d, a = p["kills"], p["deaths"], p["assists"]
    return {
        "kills": k,
        "deaths": d,
        "assists": a,
        "kda_ratio": round((k + a) / max(d, 1), 2),
    }


def extract_death_timeline(match: dict, timeline: dict, puuid: str) -> list[dict]:
    """
    Extrai todas as mortes do jogador com timestamp e posição no mapa.

    Args:
        match: JSON bruto da partida (Match v5), usado para mapear PUUID → participantId.
        timeline: JSON da timeline da partida (Match v5 /timeline).
        puuid: PUUID do jogador.

    Returns:
        Lista de dicionários, um por morte, com:
        - timestamp_ms: timestamp em milissegundos.
        - timestamp_min: timestamp em minutos (arredondado a 1 casa).
        - position: coordenadas {"x": int, "y": int} no mapa.
        - killer_id: participantId do assassino (0 = morte ambiental).

    Example:
        >>> extract_death_timeline(match, timeline, puuid)
        [{"timestamp_ms": 321857, "timestamp_min": 5.4, "position": {"x": 1724, "y": 10980}, "killer_id": 6}]
    """
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
    """
    Extrai o matchup de lane do jogador: campeão, posição e oponente direto.

    Args:
        match: JSON bruto da partida (Match v5).
        puuid: PUUID do jogador.

    Returns:
        Dicionário com champion, position e opponent_champion.
        opponent_champion = "Unknown" se nenhum oponente na mesma posição for encontrado.

    Example:
        >>> extract_lane_matchup(match, puuid)
        {"champion": "Zed", "position": "MIDDLE", "opponent_champion": "Lux"}
    """
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
