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
            dados_base = carregar_dados_financeiros()
            frase_original = user_input.strip()
            tem_interrogacao = "?" in frase_original
            termo_limpo = normalizar_texto(frase_original.replace("?", ""))
            bot_response = ""

            # Mapas de respostas
            respostas_tudo_bem = {
                True: """Tudo excelente comigo, parceiro! Obrigado por perguntar. 
E com você, tudo certinho? 😊

Estou pronto para te guiar pelas opções conceituais de Renda Fixa da minha base. 
Gostaria de começar entendendo sobre CDB, LCI/LCA ou Tesouro Direto?""",
                False: """Maravilha! Fico feliz que esteja tudo joia por aí. Vamos direto ao ponto! 🎯

Como seu guia de educação financeira, posso te explicar os conceitos do nosso catálogo 
(CDB, Letras de Crédito, Títulos Públicos, Debêntures, etc.).

Para direcionarmos o nosso papo, você prefere focar em segurança absoluta, conhecer opções 
isentas de Imposto de Renda ou títulos para o longo prazo?"""
            }

            # Lista expandida de gatilhos
            gatilhos_tudo_bem = [
                "tudo bem", "tudo bom", "tudo joia", "tudo otimo", "tudo certo", "tudo beleza",
                "tudo suave", "tudo tranquilo", "tudo belezinha", "tudo sussa", "joia", "otimo",
                "suave", "tranquilo", "tudo certinho", "certinho", "tudo cerinho", "td bem", "td certo"
            ]
            gatilhos_saudacoes = ["oi", "ola", "bom dia", "boa tarde", "boa noite", "eae", "opa", "salve", "fala"]
            gatilhos_concordancia = ["sim", "entendi", "ok", "beleza", "com certeza", "bora", "vamos", "pode ser", "fechou", "demoro"]

            # Regras de resposta
            if any(g in termo_limpo for g in gatilhos_tudo_bem):
                bot_response = respostas_tudo_bem[tem_interrogacao]
            elif any(g in termo_limpo for g in gatilhos_saudacoes):
                bot_response = """Olá! Tudo ótimo por aqui! É um prazer falar com você. 👋

Estou aqui para tirar suas dúvidas conceituais sobre o mercado de Renda Fixa.
O que você gostaria de explorar ou entender melhor hoje?"""
            elif any(g == termo_limpo for g in gatilhos_concordancia):
                bot_response = """Excelente! Então vamos continuar focados no aprendizado.

Para te guiar melhor, me conta: qual conceito de investimento você

