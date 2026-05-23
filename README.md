# LoL Match Analyzer

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=flat&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&logoColor=white)
![Riot API](https://img.shields.io/badge/Riot%20API-Match%20v5-D32936?style=flat&logo=riotgames&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?style=flat&logo=pytest&logoColor=white)

Dado um Riot ID (ex: `Faker#KR1`), o sistema busca a última partida ranqueada, extrai métricas de desempenho e um agente LangChain retorna **3 insights acionáveis em português**.

**Problema:** Jogadores de elos baixos têm dificuldade em identificar os próprios erros pós-partida.  
**Solução:** Análise automática via LLM com feedback direto e específico.

---

## Como funciona

```
Riot ID
  → API Riot (Account v1)     → PUUID
  → API Riot (Match v5)       → JSON da partida + timeline
  → Extratores (extractors.py) → KDA, matchup de lane, timeline de mortes
  → Agente LangChain           → 3 insights em pt-BR
```

---

## Pré-requisitos

- Python 3.11+
- [Chave de API da Riot](https://developer.riotgames.com/) (dura 24h, renovação gratuita)
- Chave de API da OpenAI

---

## Instalação

```bash
git clone https://github.com/seu-usuario/lol-match-analyzer
cd lol-match-analyzer

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edite .env com suas chaves
```

---

## Uso

```python
from src.riot_client import get_last_ranked_match, get_match_timeline
from src.extractors import extract_kda, extract_lane_matchup, extract_death_timeline

match = get_last_ranked_match("Matemático#1689")
match_id = match["metadata"]["matchId"]
timeline = get_match_timeline(match_id)

# Obter PUUID separadamente (ou cachear após primeira chamada)
puuid = "..."

print(extract_kda(match, puuid))
# {"kills": 0, "deaths": 5, "assists": 3, "kda_ratio": 0.6}

print(extract_lane_matchup(match, puuid))
# {"champion": "Twitch", "position": "JUNGLE", "opponent_champion": "Shaco"}

print(extract_death_timeline(match, timeline, puuid))
# [{"timestamp_ms": 321857, "timestamp_min": 5.4, "position": {...}, "killer_id": 6}, ...]
```

---

## Estrutura

```
lol-match-analyzer/
├── src/
│   ├── riot_client.py   # Busca partida e timeline via API da Riot
│   └── extractors.py    # Extrai KDA, matchup de lane, timeline de mortes
├── tests/
│   └── test_extractors.py  # Testes unitários com respostas mockadas
├── .env.example
├── requirements.txt
└── README.md
```

---

## Extratores implementados

### `extract_kda(match, puuid) → dict`
Retorna kills, deaths, assists e KDA ratio do jogador.

```python
{"kills": 7, "deaths": 3, "assists": 5, "kda_ratio": 4.0}
```

### `extract_lane_matchup(match, puuid) → dict`
Retorna campeão do jogador, posição e campeão oponente na lane.

```python
{"champion": "Zed", "position": "MIDDLE", "opponent_champion": "Lux"}
```

### `extract_death_timeline(match, timeline, puuid) → list[dict]`
Retorna cada morte com timestamp em minutos, posição no mapa e ID do assassino.

```python
[
  {"timestamp_ms": 321857, "timestamp_min": 5.4, "position": {"x": 1724, "y": 10980}, "killer_id": 6},
  ...
]
```

> **Nota:** Requer chamada separada a `get_match_timeline(match_id)` para obter os dados de timeline.

---

## Testes

```bash
python -m pytest tests/ -v
```

Dois testes unitários mocam a resposta da API da Riot e verificam:
- KDA calculado corretamente (incluindo ratio com deaths=0)
- Timeline de mortes filtra apenas mortes do jogador (ignora mortes de oponentes)

---

## Diagrama conceitual

[Ver no draw.io](https://app.diagrams.net/?src=about#G1TuuHKcZPKMZPk16GINhOsTfruHM2XTQT#%7B%22pageId%22%3A%22VkK2OuwKXaiVj8S8FYke%22%7D)
