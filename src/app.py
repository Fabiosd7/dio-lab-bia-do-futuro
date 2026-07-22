import streamlit as st
import requests

st.title("Meu Assistente Virtual")
st.write("Conectado com IA real via OpenRouter!")

api_key = st.secrets.get("OPENROUTER_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Digite sua mensagem..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    if not api_key:
        st.error("Chave de API não configurada nos Secrets do Streamlit!")
    else:
        with st.spinner("Pensando..."):
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "meta-llama/llama-3-8b-instruct:free",
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                }
                
                # Fazendo a requisição direta via HTTP POST
                url = "https://openrouter.ai"
                response = requests.post(url, headers=headers, json=payload)
                
                if response.status_code == 200:
                    dados = response.json()
                    # Acessa os dados no formato de dicionário padrão do Python
                    bot_response = dados["choices"][0]["message"]["content"]
                    
                    with st.chat_message("assistant"):
                        st.write(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    st.error(f"Erro na API ({response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Erro ao processar resposta: {str(e)}")



