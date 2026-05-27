# Smartstream AI

Smartstream AI é um agente de inteligência artificial, capaz de aprender conteúdos em PDF e responder perguntas, e executar ferramentas de acordo com o que for solicitado.
Smartstream foi criado com streamlit para interação, e langchain, para treinamento do LLM.
É possível escolher qual LLM usar, e qual modelo de embedding, no arquivo llm_config.
Recomendo fortemente o GPT-OSS:20b, pois possui boa execução de tools, precisão nas respostas, e roda bem na maioria das máquinas.


## Tecnologias utilizadas

- **Frontend:** Streamlit
- **Orquestração de IA:** LangChain
- **Banco vetorial:** Chroma
- **Leitura de PDF:** PDFPlumberLoader
- **Linguagem principal:** Python
