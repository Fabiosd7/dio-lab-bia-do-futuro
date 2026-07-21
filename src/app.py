import streamlit as st

st.title("Meu Assistente com Gemini")
st.write("Interface pronta! (Modo de teste sem API ativa)")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de entrada do usuário
if user_input := st.chat_input("Digite sua mensagem aqui..."):
    # Mostra a mensagem do usuário
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Resposta simulada
    bot_response = f"Recebi seu comando: '{user_input}'. A API será ativada aqui depois!"
    
    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

