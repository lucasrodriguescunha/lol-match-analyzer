# LoL Match Analyzer

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=flat&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat&logo=openai&logoColor=white)
![Riot API](https://img.shields.io/badge/Riot%20API-Match%20v5-D32936?style=flat&logo=riotgames&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?style=flat&logo=pytest&logoColor=white)

Dado um Riot ID (ex: `Faker#KR1`), o sistema busca a última partida ranqueada e um agente LangChain retorna **3 insights acionáveis em português** sobre o desempenho do jogador.

**Problema:** Jogadores de elos baixos têm dificuldade em identificar os próprios erros pós-partida.  
**Solução:** Análise automática via LLM com feedback direto e específico.

---

## Como funciona

```
Riot ID → API Riot (Match v5) → JSON da partida → Agente LangChain → 3 insights em pt-BR
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
from src.riot_client import get_last_ranked_match

match = get_last_ranked_match("Faker#KR1")
print(match)
```

---

## Estrutura

```
lol-match-analyzer/
├── src/
│   └── riot_client.py   # Busca a última partida ranqueada via API da Riot
├── .env.example
├── requirements.txt
└── README.md
```

---

## Diagrama conceitual

[Ver no draw.io](https://app.diagrams.net/?src=about#G1TuuHKcZPKMZPk16GINhOsTfruHM2XTQT#%7B%22pageId%22%3A%22VkK2OuwKXaiVj8S8FYke%22%7D)
