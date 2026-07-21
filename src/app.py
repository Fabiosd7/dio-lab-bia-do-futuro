import streamlit as st
import requests

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
                # Cabeçalhos seguindo o padrão oficial documentado pelo OpenRouter
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io", 
                    "X-Title": "Meu Assistente Streamlit"
                }
                
                # Payload correto enviando o histórico em formato JSON
                payload = {
                    "model": "google/gemini-flash-1.5-8b:free",
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                }
                
                # Enviando usando o parâmetro 'json' do requests para garantir formatação correta
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                # Verifica se a requisição deu certo antes de tentar ler o JSON
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data["choices"][0]["message"]["content"]
                    with st.chat_message("assistant"):
                        st.write(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    # Se falhar, exibe o texto puro do erro enviado pelo servidor
                    st.error(f"Erro na API (Status {response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Falha técnica na comunicação: {str(e)}")


