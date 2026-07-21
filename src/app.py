import streamlit as st
import google.generativeai as genai
import requests
import json

# 1. Configuração de Segurança da API do Gemini
# O Streamlit vai ler a chave direto do cofre seguro (Secrets)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. Busca os dados fictícios online direto do seu GitHub
@st.cache_data
def carregar_dados_online():
    # LINK CORRIGIDO: Aponta diretamente para o seu arquivo de dados fictícios
 url_raw = "https://githubusercontent.com"

    
    try:
        resposta = requests.get(url_raw)
        return resposta.json()
    except Exception as e:
        st.error(f"Erro ao conectar com a base de dados do GitHub: {e}")
        return {}

dados_mercado = carregar_dados_online()

# 3. Prompt de Guardrails focado em Educação Financeira e Poupança
guardrails_prompt = f"""
Você é o Guia Financeiro BIA, um assistente virtual focado exclusivamente em ensinar pessoas a saírem da poupança e investirem melhor.

Sua base de conhecimento online contém estes dados de produtos e taxas simuladas:
{json.dumps(dados_mercado, ensure_ascii=False, indent=2)}

Instruções fundamentais para as suas respostas:
1. Sempre que o usuário perguntar sobre onde colocar o dinheiro, use as informações de "comparativo_poupanca" e "rentabilidade_simulada" dos dados acima para provar o quanto o produto é mais vantajoso que a poupança.
2. Seja extremamente didático. Explique siglas de forma simples (ex: explicar o que é CDI e Selic usando as taxas simuladas de {dados_mercado.get('taxas_mercado_simuladas', {}).get('CDI_ANUAL', '12%')} e {dados_mercado.get('taxas_mercado_simuladas', {}).get('SELIC_ANUAL', '12.15%')}).
3. Alerta Urgente: Se o usuário perguntar sobre "CDC", explique imediatamente que NÃO é um investimento, mas sim um financiamento/empréstimo que tira dinheiro do bolso dele.
4. Nunca mude de assunto. Se perguntarem sobre receitas culinárias, futebol ou programação, recuse educadamente e chame o usuário de volta para o aprendizado sobre investimentos.
"""

# 4. Interface Gráfica (GUI) com Streamlit
st.set_page_config(page_title="Guia Financeiro BIA", page_icon="💰")

st.title("💰 BIA - Seu Guia de Investimentos Online")
st.subheader("Aprenda a fazer seu dinheiro render mais que a poupança!")
st.write("Consulte informações em tempo real sobre CDB, LCI, LCA, Tesouro Direto e descubra as melhores vantagens.")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens salvas na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada de texto do usuário
if pergunta := st.chat_input("Ex: Vale mais a pena colocar dinheiro no CDB ou na Poupança?"):
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})

    # Junta as regras com a pergunta
    contexto_envio = f"{guardrails_prompt}\n\nPergunta do Usuário: {pergunta}"
    
    with st.chat_message("assistant"):
        with st.spinner("Analisando produtos bancários..."):
            try:
                response = model.generate_content(contexto_envio)
                resposta_ia = response.text
                st.markdown(resposta_ia)
                st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
            except Exception as e:
                st.error(f"Erro ao processar sua resposta com a Inteligência Artificial: {e}")
