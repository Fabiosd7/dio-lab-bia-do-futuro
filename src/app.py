import streamlit as st
import json
import os
import unicodedata
from cerebras.cloud.sdk import Cerebras

# Configuração da página Streamlit (DEVE ser o primeiro comando Python do arquivo)
st.set_page_config(page_title="Gui - Guia Financeiro", page_icon="🤖", layout="centered")

# Inicializa o cliente oficial da Cerebras puxando a chave salva nos Secrets
try:
    client = Cerebras(api_key=st.secrets["CEREBRAS_API_KEY"])
except Exception:
    client = None

# Parâmetros fixos de identidade e compliance do Gui
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
st.write("Interface activa com Inteligência Artificial Ultrarrápida da Cerebras!")

# Barra Lateral (Menu Esquerdo) com as regras de Compliance
with st.sidebar:
    st.header("⚠️ Limitações Declaradas")
    for limitacao in DADOS_GUI["limitacoes"]:
        st.markdown(f"- {limitacao}")
    st.divider()
    st.caption("Repositório: Fabiosd7/dio-lab-bia-do-futuro")

# Função interna para ler o arquivo JSON completo da pasta data/
def carregar_dados_financeiros():
    caminho_json = os.path.join("data", "produtos_financeiros.json")
    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"produtos_renda_fixa": []}

# Função auxiliar para normalizar texto
def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# Inicializa o histórico do chat se for a primeira vez abrindo
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": DADOS_GUI["saudacao"]}]

# Exibe na tela o histórico de mensagens guardadas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Caixa de texto para o usuário digitar a pergunta
if user_input := st.chat_input("Digite sua dúvida sobre Renda Fixa aqui..."):
    
    # 1. Mostra a pergunta do usuário na tela e salva no histórico
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Resposta do Assistente Inteligente Gui (Processamento da IA Cerebras + RAG Local)
    with st.chat_message("assistant"):
        with st.spinner("O Gui está processando..."):
            
            if client is None:
                bot_response = "Ops! A chave CEREBRAS_API_KEY não foi configurada corretamente nos Secrets do Streamlit."
            else:
                dados_base = carregar_dados_financeiros()
                
                # Engenharia de Prompt focada em compliance e anti-alucinação
                system_prompt = f"""
                Você é o {DADOS_GUI['nome']}, o {DADOS_GUI['titulo']}.
                Sua personalidade é ser {DADOS_GUI['personalidade']} e seu tom de voz deve ser obrigatoriamente {DADOS_GUI['tom_de_voz']}.
                
                DIRETRIZES DE COMPLIANCE JURÍDICO ESTREITAS:
                1. {DADOS_GUI['limitacoes']}
                2. {DADOS_GUI['limitacoes']}
                3. {DADOS_GUI['limitacoes']}
                4. Sempre que explicar algo, reforce de forma sutil que você não faz recomendações diretas, apenas apresenta conceitos educativos.
                
                REGRA DE ANTI-ALUCINAÇÃO (RAG):
                Você deve responder as dúvidas dos usuários utilizando prioritariamente como única fonte da verdade o [BANCO DE DADOS DE PRODUTOS] abaixo. 
                Se o usuário perguntar sobre ações, criptomoedas, fundos imobiliários ou qualquer produto fora deste arquivo, diga de forma amigável que seu escopo atual é restrito a conceitos de Renda Fixa.
                
                [BANCO DE DADOS DE PRODUTOS]:
                {json.dumps(dados_base, ensure_ascii=False)}
                """
                
                # Monta a estrutura da conversa para a API da Cerebras
                contexto_api = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.messages:
                    contexto_api.append({"role": msg["role"], "content": msg["content"]})
                
                try:
                    # CORREÇÃO AQUI: Nome do modelo atualizado para o catálogo vigente da Cerebras
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=contexto_api,
                        temperature=0.3,
                        max_tokens=1024
                    )
                    bot_response = completion.choices.message.content
                except Exception as e:
                    bot_response = f"Desculpe, houve uma falha de conexão com a infraestrutura da Cerebras: {str(e)}"
            
            # Formata a resposta final garantindo a nota de compliance
            if DADOS_GUI["recusa_educada"] not in bot_response:
                final_response = f"{bot_response}\n\n*Nota do Gui: {DADOS_GUI['recusa_educada']}*"
            else:
                final_response = bot_response
                
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})



