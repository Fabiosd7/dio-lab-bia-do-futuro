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
            gatilhos_tudo_bem = ["tudo bem","tudo bom","tudo joia","tudo otimo","tudo certo","tudo beleza"]
            gatilhos_saudacoes = ["oi","ola","bom dia","boa tarde","boa noite","eae","opa","salve","fala"]
            gatilhos_concordancia = ["sim","entendi","ok","beleza","com certeza","bora","vamos","pode ser","fechou","demoro"]

            # Regras de resposta
            if any(g in termo_limpo for g in gatilhos_tudo_bem):
                bot_response = respostas_tudo_bem[tem_interrogacao]
            elif any(g in termo_limpo for g in gatilhos_saudacoes):
                bot_response = """Olá! Tudo ótimo por aqui! É um prazer falar com você. 👋

Estou aqui para tirar suas dúvidas conceituais sobre o mercado de Renda Fixa.
O que você gostaria de explorar ou entender melhor hoje?"""
            elif any(g == termo_limpo for g in gatilhos_concordancia):
                bot_response = """Excelente! Então vamos continuar focados no aprendizado.

Para te guiar melhor, me conta: qual conceito de investimento você tem mais curiosidade 
em entender como funciona em comparação com a Poupança tradicional?"""
            elif any(g in termo_limpo for g in ["seguranca","seguro","perder","reserva","risco","proteg","medo","garant"]):
                bot_response = """Se o seu foco principal é **segurança absoluta**, educacionalmente as melhores opções 
são o **Tesouro Selic** e os **CDBs com liquidez diária**."""
            elif any(g in termo_limpo for g in ["render mais","melhor ganho","lucro","rentabilidade","ganhar mais","rente mais","maior retorno","render","rendimento"]):
                bot_response = """Se você busca **rentabilidade mais agressiva**, opções como **Debêntures** e **CRI/CRA** 
podem aparecer. Mas atenção: não contam com a proteção do FGC e envolvem maior risco."""
            elif any(g in termo_limpo for g in ["imposto","ir","isento","leao","descont","taxa"]):
                bot_response = """Existem títulos **isentos de Imposto de Renda** para pessoa física, como **LCI/LCA** 
e alguns **CRI/CRA**."""
            elif any(g in termo_limpo for g in ["inflacao","poder de compra","ipca","preco","mercado","caro"]):
                bot_response = """Para proteger contra a inflação, o conceito ideal é o **Tesouro IPCA+**."""

            # Busca no JSON
            if bot_response == "":
                if "produtos_renda_fixa" in dados_base:
                    for prod in dados_base["produtos_renda_fixa"]:
                        sigla_norm = normalizar_texto(prod["sigla"])
                        nome_norm = normalizar_texto(prod["nome"])
                        sinonimos_norm = [normalizar_texto(s) for s in prod.get("sinonimos", [])]

                        # Verifica se o termo do usuário bate com sigla, nome ou sinônimo
                        if termo_limpo in sigla_norm or termo_limpo in nome_norm or termo_limpo in sinonimos_norm:
                            bot_response = f"""Perfeito! Deixa eu te guiar sobre o **{prod['sigla']}** ({prod['nome']}).

📊 Rentabilidade simulada: {prod['rentabilidade_simulada']}
📈 Exemplo de Simulação: {prod.get('exemplo_simulacao', 'Não disponível')}
🛡️ Perfil e Risco: Indicado para perfis {', '.join(prod['perfis_compativeis'])} com risco {prod['risco']}
⏱️ Liquidez: {prod['liquidez']}
🔒 Garantia FGC: {"Sim" if prod['garantia_FGC'] else "Não"}

💡 Comparativo com a Poupança: {prod['comparativo_poupanca']}
🎯 Objetivo: {prod['objetivo']}
🔖 Também conhecido como: {', '.join(prod['sinonimos'])}

Esses valores são apenas **simulações educativas**, para mostrar como a renda fixa supera a poupança.
"""
                            break

            # Fallback final com lista de produtos
            if bot_response == "":
                lista_opcoes = [
                    "CDB","LCI / LCA","Tesouro Selic","Tesouro IPCA+",
                    "Tesouro Pré-fixado","Tesouro RendA+","Letra de Câmbio",
                    "Fundos DI / Renda Fixa","Debêntures","CRI / CRA"
                ]
                opcoes_formatadas = "\n- " + "\n- ".join(lista_opcoes)

                bot_response = f"""Essa é uma ótima pergunta! Como seu guia, eu uso a nossa base de dados para esclarecer conceitos de Renda Fixa.

Você pode me perguntar sobre qualquer um destes produtos:
{opcoes_formatadas}

Qual deles você gostaria de compreender melhor?"""

            # Exibe e salva resposta SEMPRE
            st.write(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

