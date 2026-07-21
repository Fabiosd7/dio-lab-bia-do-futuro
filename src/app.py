import streamlit as st
import requests
import json

st.title("Meu Assistente Virtual")
st.write("Conectado com IA real via OpenRouter!")

# Recupera a chave de API salva nos segredos do Streamlit
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
                # Faz a chamada para um modelo gratuito excelente (Llama 3 8B)
                response = requests.post(
                    url="https://openrouter.ai",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    data=json.dumps({
                        "model": "meta-llama/llama-3-8b-instruct:free",
                        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    })
                )
                
                if response.status_code == 200:
                    bot_response = response.json()["choices"]["message"]["content"]
                    with st.chat_message("assistant"):
                        st.write(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Falha na conexão: {str(e)}")

