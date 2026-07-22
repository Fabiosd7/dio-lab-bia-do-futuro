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
            termo = user_input.lower().strip()
            bot_response = ""
            
            # --- CORREÇÃO AQUI: Tratamento inteligente para saudações e interações básicas ---
            if termo in ["oi", "ola", "olá", "tudo bem", "tudo bem?", "tudo bom", "bom dia", "boa tarde", "boa noite"]:
                bot_response = (
                    "Tudo ótimo por aqui! É um prazer conversar com você. 👍\n\n"
                    "Estou super pronto para te guiar e tirar suas dúvidas sobre os conceitos de Renda Fixa "
                    "(como CDB, LCI, LCA, Tesouro Direto e outros).\n\n"
                    "Me conta: você quer entender mais sobre qual desses investimentos hoje?"
                )
            
            # Mapeamento de intenções de busca do usuário por palavras-chave semânticas
            elif "segurança" in termo or "seguro" in termo or "perder" in termo or "reserva" in termo:
                bot_response = (
                    "Deixa eu te guiar de um jeito simples! Se o seu foco principal é **segurança absoluta** e proteção contra perdas, "
                    "educacionalmente as melhores opções da nossa base são o **Tesouro Selic** e os **CDBs com liquidez diária**.\n\n"
                    "O Tesouro Selic é garantido pelo Governo Federal (o que o torna o ativo mais seguro do país), enquanto o CDB possui a proteção do Fundo Garantidor de Crédito (FGC) para valores até R$ 250 mil. "
                    "Ambos rendem quase o dobro da Poupança tradicional mantendo seu dinheiro protegido."
                )
            elif "render mais" in termo or "melhor ganho" in termo or "lucro" in termo or "rentabilidade" in termo:
                bot_response = (
                    "Olha, se você busca uma **rentabilidade mais agressiva** dentro da Renda Fixa, o mercado te oferece opções teóricas como as **Debêntures** e os títulos de **CRI / CRA**.\n\n"
                    "Esses produtos costumam render acima de 115% do CDI ou IPCA + Taxas Altas porque financiam empresas privadas. "
                    "Mas atenção ao detalhe técnico: eles possuem maior risco e **não contam com a proteção do FGC**, sendo indicados para prazos mais longos."
                )
            elif "imposto" in termo or "ir" in termo or "isento" in termo:
                bot_response = (
                    "Deixa o Gui te explicar um detalhe que faz muita diferença no bolso! Se você quer fugir do Imposto de Renda, "
                    "existem títulos criados para incentivar setores da economia que são **100% isentos de Imposto de Renda** para pessoa física.\n\n"
                    "São as **LCI / LCA** (emitidas por bancos e protegidas pelo FGC) e os **CRI / CRA** (crédito privado). "
                    "Como o governo não desconta nada do seu lucro na hora do resgate, o rendimento líquido final costuma ser muito vantajoso comparado a um CDB comum."
                )
            elif "inflação" in termo or "poder de compra" in termo or "ipca" in termo:
                bot_response = (
                    "Se a sua preocupação é proteger o seu dinheiro contra o aumento dos preços no supermercado, o conceito ideal para você é o **Tesouro IPCA+**.\n\n"
                    "Esse título público rende uma taxa fixa mais a variação da inflação oficial (IPCA). Isso garante matematicamente "
                    "que o seu dinheiro nunca vai perder o poder de compra ao longo dos anos, sendo uma excelente opção conceitual para planos de médio e longo prazo."
                )
            else:
                # Varre o JSON procurando por siglas diretas se o usuário digitar o nome do produto específico
                produto_encontrado = None
                if "produtos_renda_fixa" in dados_base:
                    for prod in dados_base["produtos_renda_fixa"]:
                        if prod["sigla"].lower() in termo or prod["nome"].lower() in termo:
                            produto_encontrado = prod
                            break
                
                if produto_encontrado:
                    bot_response = (
                        f"Perfeito! Deixa eu te guiar de um jeito simples sobre o **{produto_encontrado['sigla']}** ({produto_encontrado['nome']}).\n\n"
                        f"📊 *Rentabilidade simulada:* {produto_encontrado['rentabilidade_simulada']}.\n"
                        f"🛡️ *Perfil e Risco:* Indicado para perfis {', '.join(produto_encontrado['perfis_compativeis'])} com risco {produto_encontrado['risco']}.\n"
                        f"⏱️ *Liquidez:* {produto_encontrado['liquidez']}.\n\n"
                        f"💡 *Comparativo com a Poupança:* {produto_encontrado['comparativo_poupanca']}"
                    )
                else:
                    # Fallback consultivo padrão se a pergunta for muito genérica
                    bot_response = (
                        "Entendi perfeitamente sua dúvida! Como seu amigo inteligente de educação financeira, "
                        "posso te explicar de forma simples todos os conceitos do mercado de Renda Fixa.\n\n"
                        "Para eu te dar a explicação conceitual perfeita, me conta: você prioriza **segurança absoluta**, "
                        "quer um investimento que seja **isento de Imposto de Renda** ou busca algo focado em **longo prazo**?"
                    )
            
            # Adiciona a recusa educada obrigatória de compliance no final de todos os fluxos
            final_response = f"{bot_response}\n\n*Nota do Gui: {DADOS_GUI['recusa_educada']}*"
            
            st.write(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})




