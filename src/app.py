import streamlit as st
import json
import os

# Configuração da página Streamlit (DEVE ser o primeiro comando Python do arquivo)
st.set_page_config(page_title="Gui - Guia Financeiro", page_icon="🤖", layout="centered")

# Parâmetros fixos de identidade e compliance do Gui (Baseados no seu documento)
DADOS_GUI = {
    "nome": "Gui",
    "titulo": "Guia Financeiro e Educador",
    "personalidade": "Consultivo, direto, educador e paciente",
    "tom_de_voz": "Informal, acessível, leve e profundamente didático",
    "saudacao": "Olá! Tudo Bem?! Sou o Gui, seu educador financeiro. Como posso te ajudar a organizar seu dinheiro hoje?",
    "recusa_educada": "Não posso recomendar onde investir, mas o Gui te explica como cada tipo funciona!",
    "limitacoes": [
        "NÃO realiza análise ou recomendação de investimentos.",
        "NÃO interage com dados sensíveis (LGPD).",
        "NÃO substitui consultoria certificada por profissionais."
    ]
}

# Título e cabeçalho da interface do usuário
st.title(f"🤖 {DADOS_GUI['nome']} - {DADOS_GUI['titulo']}")
st.write("Interface ativa e pronta para uso!")

# Barra Lateral (Menu Esquerdo) com as regras de Compliance visíveis o tempo todo
with st.sidebar:
    st.header("⚠️ Limitações Declaradas")
    for limitacao in DADOS_GUI["limitacoes"]:
        st.markdown(f"- {limitacao}")
    st.divider()
    st.caption("Repositório: Fabiosd7/dio-lab-bia-do-futuro")

# Função interna para ler o arquivo JSON que está na pasta data/
def carregar_dados_financeiros():
    # Procura o arquivo na pasta 'data' a partir da raiz do projeto
    caminho_json = os.path.join("data", "produtos_financeiros.json")
    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Retorno vazio de segurança caso o arquivo suma ou dê erro de leitura
        return {"produtos_renda_fixa": []}

# Inicializa o histórico do chat na memória do Streamlit se for a primeira vez abrindo
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": DADOS_GUI["saudacao"]}]

# Exibe na tela todo o histórico de mensagens guardadas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Caixa de texto para o usuário digitar a pergunta
if user_input := st.chat_input("Digite sua dúvida sobre Renda Fixa aqui..."):
    
    # 1. Mostra a pergunta do usuário na tela e salva no histórico
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Resposta do Assistente Gui baseada no banco de dados local
    with st.chat_message("assistant"):
        with st.spinner("O Gui está consultando a base de conhecimento..."):
            
            # Carrega os produtos salvos no JSON
            dados_base = carregar_dados_financeiros()
            termo_usuario = user_input.lower()
            resposta_encontrada = ""
            
            # Varre o JSON procurando se o usuário mencionou a sigla ou nome de algum produto
            if "produtos_renda_fixa" in dados_base:
                for produto in dados_base["produtos_renda_fixa"]:
                    if produto["sigla"].lower() in termo_usuario or produto["nome"].lower() in termo_usuario:
                        resposta_encontrada = (
                            f"Deixa eu te guiar de um jeito simples sobre o **{produto['sigla']}** ({produto['nome']}).\n\n"
                            f"📊 *Rentabilidade teórica:* {produto['rentabilidade_simulada']}.\n"
                            f"🛡️ *Risco e Liquidez:* Risco {produto['risco']} com resgate {produto['liquidez']}.\n\n"
                            f"💡 *Comparativo:* {produto['comparativo_poupanca']}"
                        )
                        break
            
            # Se encontrar o produto, formata a resposta pedagógica com a limitação legal
            if resposta_encontrada:
                bot_response = f"{resposta_encontrada}\n\n*Nota do Gui: {DADOS_GUI['recusa_educada']}*"
            else:
                # Resposta genérica padrão caso não identifique um produto específico do banco de dados
                bot_response = (
                    "Entendi sua dúvida! Como seu guia de educação financeira, posso te explicar os conceitos "
                    "de investimentos como CDB, LCI, LCA, Tesouro Selic ou Debêntures que estão no meu banco de dados.\n\n"
                    "Qual desses conceitos você gostaria que eu te explicasse de forma simples agora?"
                )
            
            # Mostra a resposta do Gui na tela e salva no histórico
            st.write(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})




