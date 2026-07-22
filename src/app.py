import streamlit as st
import json
import os
from openai import OpenAI

# Configuração da página Streamlit (DEVE ser o primeiro comando Python do arquivo)
st.set_page_config(page_title="Gui - Guia Financeiro", page_icon="🤖", layout="centered")

# Inicializa o cliente adaptado para o OpenRouter puxando a chave secreta dos Secrets
try:
    client = OpenAI(
        base_url="https://openrouter.ai",
        api_key=st.secrets["OPENROUTER_API_KEY"]
    )
except Exception:
    client = None

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
st.write("Interface ativa e com Inteligência Artificial 100% GRATUITA integrada!")

# Barra Lateral (Menu Esquerdo) com as regras de Compliance visíveis o tempo todo
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

    # 2. Resposta do Assistente Inteligente Gui (Processamento da IA + RAG Local)
    with st.chat_message("assistant"):
        with st.spinner("O Gui está pensando na resposta..."):
            
            if client is None:
                bot_response = "Ops! A chave OPENROUTER_API_KEY não foi configurada corretamente nos Secrets do Streamlit."
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            else:
                dados_base = carregar_dados_financeiros()
                
                system_prompt = f"""
                Você é o {DADOS_GUI['nome']}, o {DADOS_GUI['titulo']}.
                Sua personalidade é ser {DADOS_GUI['personalidade']} e seu tom de voz deve ser obrigatoriamente {DADOS_GUI['tom_de_voz']}.
                
                DIRETRIZES DE COMPLIANCE JURÍDICO ESTREITAS:
                1. {DADOS_GUI['limitacoes']}
                2. {DADOS_GUI['limitacoes']}
                3. {DADOS_GUI['limitacoes']}
                4. Sempre que explicar algo, reforce de forma sutil que você não faz recomendações diretas, apenas apresenta conceitos educativos.
                
                REGRA DE ANTI-ALUCINAÇÃO (RAG):
                Você deve responder as dúvidas dos usuários utilizando prioritariamente como fonte da verdade o [BANCO DE DADOS DE PRODUTOS] abaixo. 
                Se o usuário perguntar sobre ações, criptomoedas, fundos imobiliários ou qualquer produto fora deste arquivo, diga de forma amigável que seu escopo atual é restrito a conceitos de Renda Fixa.
                
                [BANCO DE DADOS DE PRODUTOS]:
                {json.dumps(dados_base, ensure_ascii=False)}
                """
                
                contexto_api = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.messages:
                    contexto_api.append({"role": msg["role"], "content": msg["content"]})
                
                try:
                    # MUDANÇA: Usando o modelo gratuito do Gemini (muito mais robusto contra quedas)
                    completion = client.chat.completions.create(
                        model="google/gemini-2.5-flash:free",
                        messages=contexto_api,
                        temperature=0.3
                    )
                    
                    # Captura a resposta tratando se vier como texto (evitando códigos HTML) ou JSON
                    if isinstance(completion, str):
                        if "<doctype html" in completion.lower() or "<html" in completion.lower():
                            bot_response = "O servidor gratuito do OpenRouter está instável no momento. Pode tentar enviar sua mensagem novamente?"
                        else:
                            bot_response = completion
                    elif hasattr(completion, 'choices') and len(completion.choices) > 0:
                        bot_response = completion.choices[0].message.content
                    else:
                        dados_resposta = dict(completion)
                        bot_response = dados_resposta['choices'][0]['message']['content']
                        
                except Exception as e:
                    bot_response = "Opa, o servidor de IA gratuito demorou para responder. Por favor, envie sua mensagem novamente!"
                
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})




