# debug_indexacao.py
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os, glob

PASTA_PDFS = "./pdfs"
PASTA_VECTORDB = "./vectordb"
OLLAMA_URL = "http://localhost:11434"
MODELO_EMBEDDINGS = "bge-m3"

print("=== STEP 1: Testando conexão com Ollama ===")
import requests
try:
    r = requests.get(f"{OLLAMA_URL}/api/tags")
    print(f"Ollama OK — modelos: {[m['name'] for m in r.json()['models']]}")
except Exception as e:
    print(f"[ERRO] Ollama não responde: {e}")
    exit()

print("\n=== STEP 2: Testando embedding ===")
embeddings = OllamaEmbeddings(model=MODELO_EMBEDDINGS, base_url=OLLAMA_URL)
try:
    vetor = embeddings.embed_query("teste de embedding")
    print(f"Embedding OK — dimensão do vetor: {len(vetor)}")
except Exception as e:
    print(f"[ERRO] Embedding falhou: {e}")
    exit()

print("\n=== STEP 3: Verificando PDFs ===")
pdfs = glob.glob(f"{PASTA_PDFS}/*.pdf")
print(f"PDFs encontrados: {pdfs}")
if not pdfs:
    print("[ERRO] Nenhum PDF na pasta. Verifique o caminho.")
    exit()

print("\n=== STEP 4: Carregando PDFs ===")
documentos = []
for pdf in pdfs:
    try:
        loader = PDFPlumberLoader(pdf)
        docs = loader.load()
        documentos.extend(docs)
        print(f"  {pdf} → {len(docs)} página(s)")
    except Exception as e:
        print(f"  [ERRO] {pdf}: {e}")

if not documentos:
    print("[ERRO] Nenhum documento carregado.")
    exit()

print(f"\nTotal de páginas: {len(documentos)}")
print(f"Amostra do conteúdo:\n{documentos[0].page_content[:200]}")

print("\n=== STEP 5: Criando chunks ===")
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=300)
chunks = splitter.split_documents(documentos)
print(f"Total de chunks: {len(chunks)}")

print("\n=== STEP 6: Criando VectorDB ===")
os.makedirs(PASTA_VECTORDB, exist_ok=True)
try:
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PASTA_VECTORDB
    )
    print(f"VectorDB criado! Total de vetores: {db._collection.count()}")
    print(f"Arquivos em ./vectordb: {os.listdir(PASTA_VECTORDB)}")
except Exception as e:
    print(f"[ERRO] Falha ao criar VectorDB: {e}")