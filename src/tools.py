import json
from langchain_core.tools import tool
from src.riot_client import get_last_ranked_match, get_match_timeline
from src.extractors import extract_kda, extract_death_timeline, extract_lane_matchup

_match_cache: dict[str, tuple[dict, str]] = {}
_timeline_cache: dict[str, dict] = {}


def _fetch_match(riot_id: str) -> tuple[dict, str]:
    if riot_id not in _match_cache:
        _match_cache[riot_id] = get_last_ranked_match(riot_id)
    return _match_cache[riot_id]


def _fetch_timeline(match_id: str) -> dict:
    if match_id not in _timeline_cache:
        _timeline_cache[match_id] = get_match_timeline(match_id)
    return _timeline_cache[match_id]


@tool
def tool_get_kda(riot_id: str) -> str:
    """
    Get KDA stats for a player's most recent ranked match.
    Returns kills, deaths, assists, and KDA ratio.
    Input: Riot ID in 'GameName#TAG' format (e.g. 'Faker#KR1').
    """
    match, puuid = _fetch_match(riot_id)
    return json.dumps(extract_kda(match, puuid))


@tool
def tool_get_death_timeline(riot_id: str) -> str:
    """
    Get death positions and timestamps for a player's most recent ranked match.
    Shows when (minutes) and where (map coordinates) the player died each time.
    Useful for identifying risky zones and bad positioning habits.
    Input: Riot ID in 'GameName#TAG' format (e.g. 'Faker#KR1').
    """
    match, puuid = _fetch_match(riot_id)
    match_id = match["metadata"]["matchId"]
    timeline = _fetch_timeline(match_id)
    return json.dumps(extract_death_timeline(match, timeline, puuid))


@tool
def tool_get_lane_matchup(riot_id: str) -> str:
    """
    Get lane matchup info for a player's most recent ranked match.
    Returns champion played, position/role, and the direct lane opponent.
    Input: Riot ID in 'GameName#TAG' format (e.g. 'Faker#KR1').
    """
    match, puuid = _fetch_match(riot_id)
    return json.dumps(extract_lane_matchup(match, puuid))
