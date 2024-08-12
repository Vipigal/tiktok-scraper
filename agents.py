from crewai import Agent, Task, Crew
from langchain_ollama import ChatOllama
import os

os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434"
os.environ["OPENAI_MODEL_NAME"] = "llama2"
os.environ["OPENAI_API_KEY"] = ""

llm = ChatOllama(model="llama3.1", base_url="http://localhost:11434")

# Configuração do agente para classificação
agente_classificacao = Agent(
    role="Classificador de Echo Chamber",
    goal="""Identificar se o conteúdo fornecido, que é a combinacao de descricao e hashtags de um TikTok, faz parte de uma echo chamber. Considere se o topico do assunto é geralmente polarizador, como discussões sobre política, religião, vacinas, ou outras questões sociais.""",
    backstory="""Você é um especialista em identificar conteúdo brasileiro da rede social TikTok pertence a uma echo chamber ou nao.
    Você sabe que uma echo chamber é uma descrição metafórica de uma situação em que informações, ideias ou crenças são amplificadas ou reforçadas pela comunicação e repetição dentro de um sistema definido. Dentro de uma echo chamber, as fontes dominantes muitas vezes são inquestionáveis e opiniões diferentes ou concorrentes são censuradas ou desautorizadas. A maioria dos ambientes de echo chambers dependem de doutrinação e propaganda, a fim de disseminar informação, sutil ou não, de modo a atrapalhar os que estão presos na chamber e a evitar que tenham habilidades de pensamento cético necessárias para desacreditar a desinformação óbvia.
    Você tambem sabe que uma echo chamber geralmente tem como assunto um conteudo polarizador que divide opinioes e pode causar discussoes calorosas.""",
    verbose=False,
    llm=llm,
)


async def classificar_conteudo(descricao, hashtags):
    # Concatena a descrição e as hashtags em um único texto
    texto = descricao + " " + " ".join(f"#{tag}" for tag in hashtags)
    # Cria uma tarefa de classificação
    tarefa = Task(
        description=f"""Classifique o seguinte conteúdo: "{texto}". Ele pertence a uma echo chamber, considerando os critérios descritos?""",
        agent=agente_classificacao,
        expected_output="Uma string unica que pode ser echo-chamber ou nao-echo-chamber. Nao elabore nenhum tipo de resposta, apenas classifique o conteudo.",
    )

    # Configura o CrewAI com o agente e a tarefa
    crew = Crew(agents=[agente_classificacao], tasks=[tarefa], verbose=False)

    # Executa a tarefa
    resultado = await crew.kickoff_async()

    # Extrai e retorna a classificação do resultado
    classificacao = resultado.raw
    return classificacao


# Função de teste
if __name__ == "__main__":
    descricao = "O governo está sempre escondendo a verdade sobre as vacinas."
    hashtags = ["#vacinas", "#verdade", "#politica"]
    resultado = classificar_conteudo(descricao, hashtags)
    print(resultado)
