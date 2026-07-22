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
            
            tem_interrogacao = "?" in frase_original
            termo_limpo = normalizar_texto(frase_original.replace("?", ""))
            bot_response = ""
            
            # --- MAPA DE RESPOSTAS EM ESTRUTURA LINEAR ---
            respostas_tudo_bem = {
                True: "Tudo excelente comigo, parceiro! Obrigado por perguntar. E com você, tudo certinho? 😊\n\nEstou pronto para te guiar pelas opções conceituais de Renda Fixa da minha base. Gostaria de começar entendendo sobre CDB, LCI/LCA ou Tesouro Direto?",
                False: "Maravilha! Fico feliz que esteja tudo joia por aí. Vamos direto ao ponto! 🎯\n\nComo seu guia de educação financeira, posso te explicar os conceitos do nosso catálogo (CDB, Letras de Crédito, Títulos Públicos, Debêntures, etc.).\n\nPara direcionarmos o nosso papo, você prefere focar em segurança absoluta, conhecer opções isentas de Imposto de Renda ou títulos para o longo prazo?"
            }
            
            gatilhos_tudo_bem = ["tudo bem", "tudo bom", "tudo joia", "tudo otimo", "tudo certo", "tudo beleza", "tudo suave", "tudo tranquilo", "tudo belezinha", "tudo sussa", "joia", "otimo", "suave", "tranquilo"]
            gatilhos_saudacoes = ["oi", "ola", "bom dia", "boa tarde", "boa noite", "eae", "opa", "salve", "fala"]
            gatilhos_concordancia = ["sim", "entendi", "ok", "beleza", "com certeza", "bora", "vamos", "pode ser", "fechou", "demoro"]
            
            # 1. Checagem de saudações combinadas e variações de "tudo bem"
            if any(g in termo_limpo for g in gatilhos_tudo_bem):
                bot_response = respostas_tudo_bem[tem_interrogacao]
            
            # 2. Saudações simples (oi, olá)
            elif any(g in termo_limpo for g in gatilhos_saudacoes) and bot_response == "":
                bot_response = "Olá! Tudo ótimo por aqui! É um prazer falar com você. 👋\n\nEstou aqui para tirar suas dúvidas conceituais sobre o mercado de Renda Fixa.\nO que você gostaria de explorar ou entender melhor hoje?"
            
            # 3. Concordâncias (sim, ok)
            elif any(g == termo_limpo for g in gatilhos_concordancia) and bot_response == "":
                bot_response = "Excelente! Então vamos continuar focados no aprendizado.\n\nPara te guiar melhor, me conta: qual conceito de investimento você tem mais curiosidade em entender como funciona em comparação com a Poupança tradicional?"
                
            # 4. Mapeamento de intenções financeiras (Segurança)
            elif any(g in termo_limpo for g in ["seguranca", "seguro", "perder", "reserva", "risco", "proteg", "medo", "garant"]) and bot_response == "":
                bot_response = "Deixa eu te guiar de um jeito simples! Se o seu foco principal é **segurança absoluta** e proteção contra perdas, educacionalmente as melhores opções da nossa base são o **Tesouro Selic** e os **CDBs com liquidez diária**.\n\nTítulo Público Federal é garantido pelo Governo Federal (o que o torna o ativo mais seguro do país), enquanto o CDB possui a proteção do Fundo Garantidor de Crédito (FGC) para valores até R$ 250 mil. Ambos rendem quase o dobro da Poupança tradicional mantendo seu dinheiro protegido."
            
            # 5. Mapeamento de intenções financeiras (Rentabilidade)
            elif any(g in termo_limpo for g in ["render mais", "melhor ganho", "lucro", "rentabilidade", "ganhar mais", "rente mais", "maior retorno", "render", "rendimento"]) and bot_response == "":
                bot_response = "Olha, se você busca uma **rentabilidade mais agressiva** dentro da Renda Fixa, o mercado te oferece opções teóricas como as **Debêntures** e os títulos de **CRI / CRA**.\n\nEsses produtos costumam render acima de 115% do CDI ou IPCA + Taxas Altas porque financiam empresas privadas. Mas atenção ao detalhe técnico: eles possuem maior risco e **não contam com a proteção do FGC**, sendo indicados para prazos mais longos."
            
            # 6. Mapeamento de intenções financeiras (Impostos)
            elif any(g in termo_limpo for g in ["imposto", "ir", "isento", "leao", "descont", "taxa"]) and bot_response == "":
                bot_response = "Deixa o Gui te explicar um detalhe que faz muita diferença no bolso! Se você quer fugir do Imposto de Renda, existem títulos criados para incentivar setores da economia que são **100% isentos de Imposto de Renda** para pessoa física.\n\nSão as **LCI / LCA** (emitidas por bancos e protegidas pelo FGC) e os **CRI / CRA** (crédito privado). Como o governo não desconta nada do seu lucro na hora do resgate, o rendimento líquido final costuma ser muito avantajoso comparado a um CDB comum."
            
            # 7. Mapeamento de intenções financeiras (Inflação)
            elif any(g in termo_limpo for g in ["inflacao", "poder de compra", "ipca", "preco", "mercado", "caro"]) and bot_response == "":
                bot_response = "Se a sua preocupação é proteger o seu dinheiro contra o aumento dos preços no supermercado, o conceito ideal para você é o **Tesouro IPCA+**.\n\nEsse título público rende uma taxa fixa mais a variação da inflação oficial (IPCA). Isso garante matematicamente que o seu dinheiro nunca vai perder o poder de compra ao longo dos anos, sendo uma excelente opção conceitual para planos de médio e longo prazo."
            
            # 8. Busca por siglas diretas no JSON de produtos
            if bot_response == "":
                if "produtos_renda_fixa" in dados_base:
                    for prod in dados_base["produtos_renda_fixa"]:
                        sigla_norm = normalizar_texto(prod["sigla"])
                        nome_norm = normalizar_texto(prod["nome"])
                        if sigla_norm in termo_limpo or nome_norm in termo_limpo:
                            bot_response = "Perfeito! Deixa eu te guiar de um jeito simples sobre o **" + prod['sigla'] + "** (" + prod['nome'] + ").\n\n📊 *Rentabilidade simulada:* " + prod['rentabilidade_simulada'] + ".\n🛡️ *Perfil e Risco:* Indicado para perfis " + ", ".join(prod['perfis_compativeis']) + " com risco " + prod['risco'] + ".\n⏱️ *Liquidez:* " + prod['liquidez'] + ".\n\n💡 *Comparativo com a Poupança:* " + prod['comparativo_poupanca']
                            break
            
            # --- SEÇÃO FALLBACKS FINAIS (CORRIGIDO SEM NENHUM OUTRO BLOCO IF INDENTADO) ---
            if bot_response == "":
                fallback_pergunta = "Essa é uma ótima pergunta! Como seu guia, eu uso a nossa base de dados para esclarecer conceitos de Renda Fixa de forma prática.\n\nNão localizei esse termo específico no meu catálogo, mas posso te explicar as regras de CDB, Tesouro Selic, LCI/LCA ou Debêntures. Qual desses você tem interesse em compreender?"

