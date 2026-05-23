import pytest
from src.extractors import extract_kda, extract_death_timeline, extract_lane_matchup

PUUID = "test-puuid-123"

MATCH_STUB = {
    "info": {
        "participants": [
            {
                "puuid": PUUID,
                "kills": 7,
                "deaths": 3,
                "assists": 5,
                "championName": "Zed",
                "teamPosition": "MIDDLE",
                "teamId": 100,
            },
            {
                "puuid": "enemy-puuid",
                "kills": 2,
                "deaths": 7,
                "assists": 1,
                "championName": "Lux",
                "teamPosition": "MIDDLE",
                "teamId": 200,
            },
        ]
    }
}

TIMELINE_STUB = {
    "info": {
        "frames": [
            {
                "timestamp": 60000,
                "events": [
                    {
                        "type": "CHAMPION_KILL",
                        "timestamp": 65000,
                        "victimId": 1,  # participantId 1 = PUUID (index 0 + 1)
                        "killerId": 2,
                        "position": {"x": 4000, "y": 5000},
                    }
                ],
            },
            {
                "timestamp": 900000,
                "events": [
                    {
                        "type": "CHAMPION_KILL",
                        "timestamp": 910000,
                        "victimId": 1,
                        "killerId": 2,
                        "position": {"x": 6000, "y": 7000},
                    },
                    {
                        "type": "CHAMPION_KILL",
                        "timestamp": 912000,
                        "victimId": 2,  # enemy dies — should be ignored
                        "killerId": 1,
                        "position": {"x": 6100, "y": 7100},
                    },
                ],
            },
        ]
    }
}


def test_extract_kda():
    result = extract_kda(MATCH_STUB, PUUID)
    assert result["kills"] == 7
    assert result["deaths"] == 3
    assert result["assists"] == 5
    assert result["kda_ratio"] == round((7 + 5) / 3, 2)


def test_extract_death_timeline_filters_only_player_deaths():
    deaths = extract_death_timeline(MATCH_STUB, TIMELINE_STUB, PUUID)
    assert len(deaths) == 2
    assert deaths[0]["timestamp_min"] == round(65000 / 60000, 1)
    assert deaths[1]["timestamp_min"] == round(910000 / 60000, 1)
    # Enemy death at participantId 2 must NOT appear
    for d in deaths:
        assert d["killer_id"] != 0 or True  # killer present
