import streamlit as st

st.title("Meu Assistente Virtual")
st.write("Interface ativa e pronta para uso!")

# Inicializa o histórico de mensagens se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de entrada para o usuário digitar
if user_input := st.chat_input("Digite sua mensagem aqui..."):
    # Mostra a mensagem que o usuário acabou de digitar
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Resposta inteligente simulada (sem depender de servidores externos)
    bot_response = f"Olá! Recebi sua mensagem: '{user_input}'. O aplicativo Streamlit foi configurado com sucesso e a interface está respondendo perfeitamente!"
    
    # Mostra a resposta do assistente na tela
    with st.chat_message("assistant"):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})




