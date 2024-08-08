from crewai import Agent, Task, Crew
from langchain_ollama import ChatOllama
import os
os.environ["OPENAI_API_KEY"] = "NA"
os.environ['OPENAI_API_BASE']='http://localhost:11434'
os.environ['OPENAI_MODEL_NAME']='llama2'  
os.environ['OPENAI_API_KEY']=''

llm = ChatOllama(
    model = "llama3.1",
    base_url = "http://localhost:11434")

# Configuração do agente para classificação
agente_classificacao = Agent(
    role="Classificador de Conteúdo",
    goal="""Classificar o texto fornecido como opinativo ou não opinativo com base no seu conteúdo.""",
    backstory="""Você é um especialista em identificar conteúdo opinativo em postagens de redes sociais, baseado em descrições e hashtags.""",
    allow_delegation=False,
    verbose=False,
    llm=llm
)

def classificar_conteudo(descricao, hashtags):
    # Concatena a descrição e as hashtags em um único texto
    texto = descricao + " " + " ".join(f"#{tag}" for tag in hashtags)
    # Cria uma tarefa de classificação
    tarefa = Task(
        description=f"""Classifique o seguinte conteúdo: "{texto}".""",
        agent=agente_classificacao,
        expected_output="Uma string unica que pode ser Opinativo ou Não-opinativo."
    )

    # Configura o CrewAI com o agente e a tarefa
    crew = Crew(
        agents=[agente_classificacao],
        tasks=[tarefa],
        verbose=False
    )

    # Executa a tarefa
    resultado = crew.kickoff()

    # Extrai e retorna a classificação do resultado
    classificacao = resultado.raw
    return classificacao

# Função de teste
if __name__ == "__main__":
    descricao = "Esta é uma descrição de exemplo. Eu gosto do nikolas ferreira e odeio a mamata"
    hashtags = ["#teste", "#exemplo"]
    resultado = classificar_conteudo(descricao, hashtags)
    print(resultado)