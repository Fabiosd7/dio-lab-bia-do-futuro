import streamlit as st
from openai import OpenAI

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
                # Inicializa o cliente apontando para o OpenRouter
                client = OpenAI(
                    base_url="https://openrouter.ai",
                    api_key=api_key,
                )

                # Chamada correta do modelo
                response = client.chat.completions.create(
                    model="meta-llama/llama-3-8b-instruct:free",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    extra_headers={
                        "HTTP-Referer": "https://streamlit.io",
                        "X-Title": "Meu Assistente Streamlit",
                    }
                )
                
                # CORREÇÃO DA LINHA: Lendo a resposta no formato correto da biblioteca
                bot_response = response.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    
            except Exception as e:
                st.error(f"Falha na comunicação com a IA: {str(e)}")

