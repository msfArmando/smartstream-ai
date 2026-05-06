import streamlit as st
from st_html import render_titulo
from PIL import Image
from llm import inicializar, llm_response

pdf_is_loadade = None

# Cria um dicionário quando a função do agente, e a primeira mensagem
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá, como posso ajudar?"}
    ]

# Inicia o agente assim que o código é compilado
if "agente" not in st.session_state:
    with st.status("Inicializando agente..."):
        try:
            st.session_state["agente"] = inicializar()
        except FileNotFoundError as e:
            print("DEBUG 1 !!!!!!!!!!!!!!!!!!!!!!!! ENTROU.")
            st.warning("Nenhum PDF encontrado. Por favor, carregue um PDF para que o agente possa responder perguntas baseadas em seus conteúdos.")
        except Exception as e:
            st.error(f"Erro ao inicializar agente: {e}")

# Inicia uma condição para verificar se o pdf foi carregado
if "is_pdf_loaded" not in st.session_state:
    st.session_state["is_pdf_loaded"] = False

# Icone do agente
avatar_ia = Image.open("assets/page_icon.png")

# Definindo configurações da página
st.set_page_config(
    layout='centered',
    page_icon="assets/page_icon.png",
    page_title="Smartstream"
)

# Criando colunas
col1, titulo, col3 = st.columns([0.5, 25, 0.5])
with titulo:
    # Carregando html personalizado para título
    render_titulo()

# Criando colunas para o agente
col1, upload_files_col, col3 = st.columns([1, 5, 1])
with upload_files_col:

    # Criando elemento no streamlit que recebe e carrega arquivos.
    upload_files = st.file_uploader(
        "Carregar PDFs", accept_multiple_files=True, type="pdf"
    )

    # Assim que o arquivo é carregado, o streamlit reinicia automaticamente, e a variável de session state é alterada
    if upload_files:
        st.session_state["is_pdf_loaded"] = True

    # ISso garante a mensagem de status de carregando pdf não apareça na primeira execução da aplicação sem nem mesmo algum pdf ter sido carregado
    if st.session_state["is_pdf_loaded"]:
        with st.status("Carregando lista de PDFs...", expanded=True) as status:
            for pdf in upload_files:
                with st.status("Salvando PDF..."):
                    with open(f'pdfs/{pdf.name}', 'wb') as f:
                        f.write(pdf.getvalue())
            
            with st.status("Atualizando agente com novos PDFs..."):
                st.session_state["agente"] = inicializar()

            status.update(
                label="PDFs carregados com sucesso!",
                state="complete",
                expanded=False
            )


# Criando agora colunas para colocar o chat
col1, chat, col3 = st.columns([0.5, 16, 0.5])
with chat:
    with st.container(border=True, height=550, width=700):

        # Renderiza histórico de nmensagens.
        for msg in st.session_state["messages"]:
            # aqui ele busca o componente msg no dicionário messages. Se a role desse elemnto no dicionário for assistant, ele carrega o ícone avatar_ia, se for user, ele atribui o valor user.
            avatar = avatar_ia if msg["role"] == "assistant" else "user"
            # E carrega a mensagem de conteúdo de acordo com o dicionário
            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])

        # Aqui o if verifica se tem algum dado dentro do prompt, e ao mesmo tempo um valor é atribuido a variável prompt. Se nenhum valor for atribuido a variável prompt, esse bloco não é executado, se for atribuido, ele executa.
        # Basicamente, ele atribui um valor e verifica se tem esse valor ao mesmo tempo.
        if prompt := st.chat_input("Digite sua mensagem..."):

            # Adiciona mensagem do usuário
            st.session_state["messages"].append({
                "role": "user",
                "content": prompt
            })

            # Gera resposta
            with st.status("Gerando resposta..."):
                # Resposta sendo gerada pela função llm_response
                resposta = llm_response(
                    st.session_state["agente"],
                    st.session_state["messages"]
                )

            # Salva resposta
            st.session_state["messages"].append({
                "role": "assistant",
                "content": resposta
            })

            st.rerun()