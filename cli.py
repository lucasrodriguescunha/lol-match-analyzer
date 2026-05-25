import sys
from dotenv import load_dotenv
from src.agent import create_coach_agent

load_dotenv()


def main() -> None:
    if len(sys.argv) > 1:
        riot_id = sys.argv[1]
    else:
        riot_id = input("Riot ID (ex: Faker#KR1): ").strip()

    if not riot_id or "#" not in riot_id:
        print("Erro: Riot ID inválido. Use o formato 'GameName#TAG'.")
        sys.exit(1)

    print(f"\nAnalisando partida de {riot_id}...\n")
    agent = create_coach_agent()

    result = agent.invoke({
        "messages": [(
            "human",
            f"Analise a última partida ranqueada de {riot_id}. "
            "Use as ferramentas disponíveis para coletar KDA, mortes e matchup de lane. "
            "Depois forneça feedback de coach focado nos erros mais impactantes e o que fazer diferente."
        )]
    })

    output = result["messages"][-1].content
    print("\n" + "=" * 60)
    print("ANÁLISE DO COACH")
    print("=" * 60)
    print(output)
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
