import streamlit as st
import json
import os
import unicodedata

# Configuração da página Streamlit
st.set_page_config(page_title="Gui - Guia Financeiro", page_icon="🤖", layout="centered")

# Parâmetros fixos de identidade e compliance
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

# Título e cabeçalho
st.title(f"🤖 {DADOS_GUI['nome']} - {DADOS_GUI['titulo']}")
st.write("Interface ativa com Motor de Respostas Consultivas Local integrado!")

# Barra lateral
with st.sidebar:
    st.header("⚠️ Limitações Declaradas")
    for limitacao in DADOS_GUI["limitacoes"]:
        st.markdown(f"- {limitacao}")
    st.divider()
    st.caption("Repositório: Fabiosd7/dio-lab-bia-do-futuro")

# Função para carregar dados JSON
def carregar_dados_financeiros():
    caminho_json = os.path.join("data", "produtos_financeiros.json")
    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"produtos_renda_fixa": []}

# Função para normalizar texto
def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# Inicializa histórico
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": DADOS_GUI["saudacao"]}]

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Caixa de entrada
if user_input := st.chat_input("Digite sua dúvida sobre Renda Fixa aqui..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("O Gui está analisando a base de conhecimento..."):

