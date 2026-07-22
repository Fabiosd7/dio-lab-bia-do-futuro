import streamlit as st
import json
import os

# Configuração da página Streamlit (DEVE ser o primeiro comando Python do arquivo)
st.set_page_config(page_title="Gui - Guia Financeiro", page_icon="🤖", layout="centered")

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
st.write("Interface ativa com Motor de Respostas Consultivas Local integrado!")

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

    # 2. Motor de Processamento Semântico Local (Simulador de IA Generativa)
    with st.chat_message("assistant"):
        with st.spinner("O Gui está analisando a base de conhecimento..."):
            
            dados_base = carregar_dados_financeiros()
            frase_original = user_input.strip()
            termo = frase_original.lower()
            bot_response = ""
            
            tem_interrogacao = "?" in termo
            termo_limpo = termo.replace("?", "").strip()
            
            # --- CORREÇÃO DE DIÁLOGO ADAPTATIVA ---
            # Se o usuário misturar saudações (ex: "oi tudo bem?"), o código prioriza responder a saudação primeiro
            if "tudo bem" in termo_limpo or "tudo bom" in termo_limpo:
                if tem_interrogacao:
                    bot_response = """Tudo excelente comigo, obrigado por perguntar! E com você, tudo certinho? 😊

Estou pronto para te guiar pelas opções conceituais de Renda Fixa da minha base. Gostaria de começar entendendo sobre CDB, LCI/LCA ou Tesouro Direto?"""
                else:
                    bot_response = """Maravilha! Vamos em frente. 🎯

Como seu guia de educação financeira, posso te explicar os conceitos do nosso catálogo (CDB, Letras de Crédito, Títulos Públicos, Debêntures, etc.).

Para direcionarmos o papo, você prefere focar em segurança absoluta, conhecer opções isentas de Imposto de Renda ou títulos para o longo prazo?"""
            
            elif termo_limpo in ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]:
                bot_response = """Olá! Tudo ótimo por aqui! É um prazer falar com você. 👋

Estou aqui para tirar suas dúvidas conceituais sobre o mercado de Renda Fixa.
O que você gostaria de explorar ou entender melhor hoje?"""
            
            elif termo_limpo in ["sim", "entendi", "ok", "beleza", "com certeza"]:
                bot_response = """Excelente! Então vamos continuar focados no aprendizado.

Para te guiar melhor, me conta: qual conceito de investimento você tem mais curiosidade em entender como funciona em comparação com a Poupança tradicional?"""
                
            # Mapeamento de intenções de busca do usuário por palavras-chave semânticas
            elif "segurança" in termo_limpo or "seguro" in termo_limpo or "perder" in termo_limpo or "reserva" in termo_limpo:
                bot_response = """Deixa eu te guiar de um jeito simples! Se o seu foco principal é **segurança absoluta** e proteção contra perdas, educacionalmente as melhores opções da nossa base são o **Tesouro Selic** e os **CDBs com liquidez diária**.

O Tesouro Selic é garantido pelo Governo Federal (o que o torna o ativo mais seguro do país), enquanto o CDB possui a proteção do Fundo Garantidor de Crédito (FGC) para valores até R$ 250 mil. Ambos rendem quase o dobro da Poupança tradicional mantendo seu dinheiro protegido."""
            
            elif "render mais" in termo_limpo or "melhor ganho" in termo_limpo or "lucro" in termo_limpo or "rentabilidade" in termo_limpo:
                bot_response = """Olha, se você busca uma **rentabilidade mais agressiva** dentro da Renda Fixa, o mercado te oferece opções teóricas como as **Debêntures** e os títulos de **CRI / CRA**.

Esses produtos costumam render acima de 115% do CDI ou IPCA + Taxas Altas porque financiam empresas privadas. Mas atenção ao detalhe técnico: eles possuem maior risco e **não contam com a proteção do FGC**, sendo indicados para prazos mais longos."""
            
            elif "imposto" in termo_limpo or "ir" in termo_limpo or "isento" in termo_limpo:
                bot_response = """Deixa o Gui te explicar um detalhe que faz muita diferença no bolso! Se você quer fugir do Imposto de Renda, existem títulos criados para incentivar setores da economia que são **100% isentos de Imposto de Renda** para pessoa física.

São as **LCI / LCA** (emitidas por bancos e protegidas pelo FGC) e os **CRI / CRA** (crédito privado). Como o governo não desconta nada do seu lucro na hora do resgate, o rendimento líquido final costuma ser muito vantajoso comparado a um CDB comum."""
            
            elif "inflação" in termo_limpo or "poder de compra" in termo_limpo or "ipca" in termo_limpo:
                bot_response = """Se a sua preocupação é proteger o seu dinheiro contra o aumento dos preços no supermercado, o conceito ideal para você é o **Tesouro IPCA+**.

Esse título público rende uma taxa fixa mais a variação da inflação oficial (IPCA). Isso garante matematicamente que o seu dinheiro nunca vai perder o poder de compra ao longo dos anos, sendo uma excelente opção conceitual para planos de médio e longo prazo."""
            
            else:
                # Varre o JSON procurando por siglas diretas se o usuário digitar o nome do produto específico
                produto_encontrado = None
                if "produtos_renda_fixa" in dados_base:
                    for prod in dados_base["produtos_renda_fixa"]:
                        if prod["sigla"].lower() in termo_limpo or prod["nome"].lower() in termo_limpo:
                            produto_encontrado = prod
                            break
                
                if produto_encontrado:
                    bot_response = f"""Perfeito! Deixa eu te guiar de um jeito simples sobre o **{produto_encontrado['sigla']}** ({produto_encontrado['nome']}).

📊 *Rentabilidade simulada:* {produto_encontrado['rentabilidade_simulada']}.
🛡️ *Perfil e Risco:* Indicado para perfis {', '.join(produto_encontrado['perfis_compativeis'])} com risco {produto_encontrado['risco']}.
⏱️ *Liquidez:* {produto_encontrado['liquidez']}.

💡 *Comparativo com a Poupança:* {produto_encontrado['comparativo_poupanca']}"""
                else:
                    if tem_interrogacao:
                        bot_response = """Essa é uma ótima pergunta! Como seu guia, eu uso a nossa base de dados para esclarecer conceitos de Renda Fixa de forma prática.

Não localizei esse termo específico no meu catálogo, mas posso te explicar as regras de CDB, Tesouro Selic, LCI/LCA ou Debêntures. Qual desses você tem interesse em compreender?"""
                    else:
                        bot_response = """Entendi o seu ponto! Como seu amigo inteligente de educação financeira, posso te explicar de forma simples todos os conceitos do mercado de Renda Fixa.

Para direcionarmos o Macau, me conta: você prioriza segurança absoluta, quer um investimento que seja isento de Imposto de Renda ou busca algo focado em longo prazo?"""
            
            # Adiciona a recusa educada obrigatória de compliance no final de todos os fluxos
            final_response = f"{bot_response}\n\n*Nota do Gui: {DADOS_GUI['recusa_educada']}*"
            
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})




