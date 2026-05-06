## ESTE ARQUIVO LLM, É O ARQUIVO LLM BASE PARA A CRIÇÃO DE QUALQUER MODELO DE LINGUAGEM
# Ele contém a configuração do modelo, a função de indexação dos PDFs, a criação da cadeia RAG e a definição da ferramenta de busca nos documentos.
# É possível seguir este padrão para criar outros arquivos de LLM, caso queira testar com outro modelo ou outra abordagem de RAG.

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
import streamlit as st

import os
import json
from pathlib import Path

from llm_config import MODELO, MODELO_EMBEDDINGS, OLLAMA_URL

llm = ChatOllama(model=MODELO, base_url=OLLAMA_URL)
embeddings = OllamaEmbeddings(model=MODELO_EMBEDDINGS, base_url=OLLAMA_URL)

PASTA_PDFS = Path("./pdfs")
PASTA_VECTORDB = Path("./vectordb")
ARQUIVO_MANIFESTO = PASTA_VECTORDB / "manifesto.json"
ARQUIVO_DB = PASTA_VECTORDB / "chroma.sqlite3"

rag_chain = None


def carregar_manifesto():
    if not ARQUIVO_MANIFESTO.exists():
        return set()
    with open(ARQUIVO_MANIFESTO, "r") as f:
        return set(json.load(f))


def salvar_manifesto(arquivos):
    os.makedirs(PASTA_VECTORDB, exist_ok=True)
    with open(ARQUIVO_MANIFESTO, "w") as f:
        json.dump(list(arquivos), f)


def carregar_vectordb():
    if not ARQUIVO_DB.exists():
        return None

    try:
        db = Chroma(
            persist_directory=str(PASTA_VECTORDB),
            embedding_function=embeddings
        )
        if db._collection.count() == 0:
            return None
        return db
    except Exception as e:
        print(f"[ERRO] vectordb: {e}")
        return None


def indexar_pdfs_novos(vectordb=None):
    arquivos_atuais = {str(p) for p in PASTA_PDFS.glob("*.pdf")}
    arquivos_indexados = carregar_manifesto()

    novos = arquivos_atuais - arquivos_indexados

    print(f"Indexando {len(novos)} PDF(s)...")

    if not novos and vectordb is not None:
        return vectordb

    documentos = []
    with st.status("Indexando PDFs...", expanded=True):
        for arquivo in novos:
            loader = PDFPlumberLoader(arquivo)
            documentos.extend(loader.load())

    with st.status("Dividindo PDFs em chunks..."):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=300
        )
        chunks = splitter.split_documents(documentos)

    try:
        if vectordb is None:
            with st.status("Criando banco de dados vetorial...") as status:
                vectordb = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=str(PASTA_VECTORDB)
                )
        else:
            with st.status("Atualizando banco de dados vetorial..."):
                vectordb.add_documents(chunks)

        with st.status("Salvando manifesto..."):
            salvar_manifesto(arquivos_atuais)

        print(f"Chunks: {vectordb._collection.count()}")
    except Exception as e:
        print(f"[ERRO indexação]: {e}")
        raise e

    return vectordb


def criar_rag_chain(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Responda usando APENAS o contexto abaixo. "
         "Se não encontrar, diga: 'Não encontrei essa informação nos documentos.'\n\n"
         "Contexto:\n{context}"),
        ("human", "{input}")
    ])

    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

    combine_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, combine_chain)


@tool
def buscar_nos_documentos(pergunta: str) -> str:
    """
    Busca informações dentro dos documentos PDF indexados.

    Use esta ferramenta quando a pergunta do usuário estiver relacionada
    a conteúdos presentes nos documentos carregados.

    Parâmetros:
    - pergunta: pergunta do usuário

    Retorna:
    - resposta baseada nos documentos ou mensagem de ausência
    """
    global rag_chain

    print("🔎 Tool chamada")

    if rag_chain is None:
        return "Nenhum documento indexado."

    resultado = rag_chain.invoke({"input": pergunta})
    return resultado["answer"]


def inicializar():
    global rag_chain

    vectordb = carregar_vectordb()
    vectordb = indexar_pdfs_novos(vectordb)

    if vectordb:
        rag_chain = criar_rag_chain(vectordb)
    else:
        rag_chain = None

    tools = [buscar_nos_documentos]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente útil que usa ferramentas quando necessário."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return executor


def llm_response(agente, messages):
    ultima_msg = messages[-1]["content"]

    resposta = agente.invoke({
        "input": ultima_msg
    })

    return resposta["output"]