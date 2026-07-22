import streamlit as st
import json
import os
import unicodedata

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

# Função auxiliar para remover acentos e deixar o texto limpo para comparação
def normalizar_texto(texto):
    texto = texto.lower().strip()
    # Remove acentos (ex: ó -> o, á -> a, ç -> c)
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

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
            
            # Identifica se o usuário usou ponto de interrogação antes de limpar a frase
            tem_interrogacao = "?" in frase_original
            
            # Limpa e normaliza o texto (remove ?, acentos e deixa tudo minúsculo)
            termo_limpo = normalizar_texto(frase_original.replace("?", ""))
            bot_response = ""
            
            # --- DICIONÁRIO EXPANDIDO DE SITUAÇÕES E VARIADAS GÍRIAS BRASILEIRAS ---
            dicionario_saudacoes = ["oi", "ola", "bom dia", "boa tarde", "boa noite", "eae", "opa", "salve", "fala", "coirmandade", "tudo bem", "tudo bom"]
            
            dicionario_tudo_joia = [
                "tudo joia", "tudo otimo", "tudo 100", "tudo certo", "tudo bem por aqui", 
                "tudo beleza", "tudo suave", "tudo tranquilo", "tudo belezinha", "tudo sussa",
                "ta tudo bem", "ta tudo joia", "ta tudo certo", "por aqui tudo bem", "por aqui tudo certo",
                "joia", "otimo", "beleza", "suave", "tranquilo", "100%", "perfeito"
            ]
            
            dicionario_concordancia = ["sim", "entendi", "ok", "beleza", "com certeza", "bora", "vamos", "pode ser", "fechou", "demoro"]
            
            dicionario_seguranca = ["seguranca", "seguro", "perder", "reserva", "risco", "proteg", "medo", "garant"]
            dicionario_rentabilidade = ["render mais", "melhor ganho", "lucro", "rentabilidade", "ganhar mais", "rende mais", "maior retorno"]
            dicionario_imposto = ["imposto", "ir", "isento", "leao", "descont", "taxa"]
            dicionario_inflacao = ["inflacao", "poder de compra", "ipca", "preço", "mercado", "caro"]

            # --- FLUXO DE TOMADA DE DECISÃO INTELIGENTE ---
            
            # 1. Se o usuário estiver perguntando se está tudo bem ("Tudo joia?", "Tudo bem?")
            if any(exp in termo_limpo for exp in ["tudo bem", "tudo bom", "tudo joia", "tudo beleza", "tudo suave", "tudo tranquilo"]) and tem_interrogacao:
                bot_response = """Tudo excelente comigo, parceiro! Obrigado por perguntar. E com você, tudo certinho? 😊

Estou pronto para te guiar pelas opções conceituais de Renda Fixa da minha base. Gostaria de começar entendendo sobre CDB, LCI/LCA ou Tesouro Direto?"""
            
            # 2. Se o usuário estiver apenas respondendo que está tudo bem/tudo joia (Afirmação)
            elif any(termo_limpo == exp or termo_limpo.startswith(exp) or exp in termo_limpo for exp in dicionario_tudo_joia):
                bot_response = """Maravilha! Fico feliz que esteja tudo joia por aí. Vamos direto ao ponto! 🎯

Como seu guia de educação financeira, posso te explicar os conceitos do nosso catálogo (CDB, Letras de Crédito, Títulos Públicos, Debêntures, etc.).

Para direcionarmos o nosso papo, você prefere focar em segurança absoluta, conhecer opções isentas de Imposto de Renda ou títulos para o longo prazo?"""
            
            # 3. Saudações genéricas (Oi, Olá, Eae)
            elif any(saud in termo_limpo for saud in dicionario_saudacoes):
                bot_response = """Olá! Tudo ótimo por aqui! É um prazer falar com você. 👋

Estou aqui para tirar suas dúvidas conceituais sobre o mercado de Renda Fixa.
O que você gostaria de explorar ou entender melhor hoje?"""
            
            # 4. Respostas de concordância simples (Sim, Fechou, Ok)
            elif any(conc == termo_limpo for conc in dicionario_concordancia):
                bot_response = """Excelente! Então vamos continuar focados no aprendizado.

Para te guiar melhor, me conta: qual conceito de investimento você tem mais curiosidade em entender como funciona em comparação com a Poupança tradicional?"""
                
            # 5. Mapeamento de intenções financeiras (Segurança)
            elif any(seg in termo_limpo for seg in dicionario_seguranca):
                bot_response = """Deixa eu te guiar de um jeito simples! Se o seu foco principal é **segurança absoluta** e proteção contra perdas, educacionalmente as melhores opções da nossa base são o **Tesouro Selic** e os **CDBs com liquidez diária**.

O Tesouro Selic é garantido pelo Governo Federal (o que o torna o ativo mais seguro do país), enquanto o CDB possui a proteção do Fundo Garantidor de Crédito (FGC) para valores até R$ 250 mil. Ambos rendem quase o dobro da Poupança tradicional mantendo seu dinheiro protegido."""
            
            # 6. Mapeamento de intenções financeiras (Rentabilidade)
            elif any(rent in termo_limpo for rent in dicionario_rentabilidade):
                bot_response = """Olha, se você busca uma **rentabilidade mais agressiva** dentro da Renda Fixa, o mercado te oferece opções teóricas como as **Debêntures** e os títulos de **CRI / CRA**.

Esses produtos costumam render acima de 115% do CDI ou IPCA + Taxas Altas porque financiam empresas privadas. Mas atenção ao detalhe técnico: eles possuem maior risco e **não contam com a proteção do FGC**, sendo indicados para prazos mais longos."""
            
            # 7. Mapeamento de intenções financeiras (Impostos)
            elif any(imp in termo_limpo for imp in dicionario_imposto):
                bot_response = """Deixa o Gui te explicar um detalhe que faz muita diferença no bolso! Se você quer fugir do Imposto de Renda, existem títulos criados para incentivar setores da economia que são **100% isentos de Imposto de Renda** para pessoa física.

São as **LCI / LCA** (emitidas por bancos e protegidas pelo FGC) e os **CRI / CRA** (crédito privado). Como o governo não desconta nada do seu lucro na hora do resgate, o rendimento líquido final costuma ser muito avantajoso comparado a um CDB comum."""
            
            # 8. Mapeamento de intenções financeiras (Inflação)
            elif any(inf in termo_limpo for inf in dicionario_inflacao):
                bot_response = """Se a sua preocupação é proteger o seu dinheiro contra o aumento dos preços no supermercado, o conceito ideal para você é o **Tesouro IPCA+**.

Esse título público rende uma taxa fixa mais a variação da inflação oficial (IPCA). Isso garante matematicamente que o seu dinheiro nunca vai perder o poder de compra ao longo dos anos, sendo uma excelente opção conceitual para planos de médio e longo prazo."""
            
            else:
                # 9. Busca exata de produtos no JSON (CDB, LCA, CRI, etc.)
                produto_encontrado = None
                if "produtos_renda_fixa" in dados_base:
                    for prod in dados_base["produtos_renda_fixa"]:
                        # Normaliza também a sigla e o nome do produto para evitar erros de acentuação
                        sigla_norm = normalizar_texto(prod["sigla"])
                        nome_norm = normalizar_texto(prod["nome"])





