# Smartstream AI

Smartstream AI é um agente de inteligência artificial, capaz de aprender conteúdos em PDF e responder perguntas, e executar ferramentas de acordo com o que for solicitado.
Smartstream foi criado com streamlit para interação, e langchain, para treinamento do LLM.
É possível escolher qual LLM usar, e qual modelo de embedding, no arquivo llm_config.
Recomendo fortemente o GPT-OSS:20b, pois possui boa execução de tools, precisão nas respostas, e roda bem na maioria das máquinas.

Meu setup para rodar o GPT-OSS:20b tranquilamente:
- GPU: RX 6750 XT
- CPU: Ryzen 7 5700X
- Memória RAM: 32gb

## Tecnologias utilizadas

- **Frontend:** Streamlit
- **Orquestração de IA:** LangChain
- **Modelo de linguagem:** ChatOllama
- **Embeddings:** OllamaEmbeddings
- **Banco vetorial:** Chroma
- **Leitura de PDF:** PDFPlumberLoader
- **Chunking de texto:** RecursiveCharacterTextSplitter
- **Agentes e tools:** AgentExecutor, create_tool_calling_agent
- **Linguagem principal:** Python
