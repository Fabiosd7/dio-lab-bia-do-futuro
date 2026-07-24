# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Sim,mas com algumas limitações  |
| **Segurança** | O agente evitou inventar informações? | sim, já que estava se baseando em apenas seus bancos de dados |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Não foi baseado apenas no perfil do cliente,mas sim no seu interesse |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`, lembre-se de contextualizar os participantes sobre o **cliente fictício** representado nesses dados.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Valor baseado no `transacoes.csv`
- **Resultado:** [ ] Correto  [x] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** (O agente sugere avaliar os ativos disponíveis na base e explica as características pedagógicas de cada um)
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** (A resposta padrão direciona o usuário de volta para os produtos mapeados)
- **Resultado:** [x] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** (Aciona o fallback instruindo sobre quais produtos estão disponíveis no catálogo)
- **Resultado:** [x] Correto  [ ] Incorreto 

---

## Resultados

Após os testes, registre suas conclusões:
## 🚀 Resultados e Demonstração

O projeto foi concluído com sucesso e está **100% funcional e online**. A arquitetura local baseada em mapeamento de palavras-chave eliminou os gargalos de memória do servidor gratuito do Streamlit, garantindo respostas instantâneas e sem custos de API.

### 🌐 Link do Aplicativo Online
Você pode testar o "Gui" rodando ao vivo diretamente no navegador através do link abaixo:
👉 **https://streamlit.app** 

### 📸 Demonstração Visual
Abaixo está o registro do chat respondendo consultas sobre Renda Fixa de forma estruturada, didática e em conformidade com as regras educativas:
<img width="378" height="761" alt="image" src="https://github.com/user-attachments/assets/740034ee-1c6d-4031-978e-c91a477ad30f" />

!(https://githubusercontent.com)

**O que funcionou bem:**
-O que funcionou muito bem no projeto foi a resiliência e estabilidade da interface desenvolvida em Streamlit, associada à implementação bem-sucedida do Continuous Deployment (implantação contínua) via GitHub no Streamlit Community Cloud. A mudança estratégica para um motor de busca local e dicionário estático em Python se mostrou uma excelente solução de engenharia: ela eliminou completamente o tempo de latência nas respostas e resolveu o gargalo de consumo de memória RAM do servidor gratuito, garantindo que o aplicativo ficasse 100% online e funcional. Além disso, a estruturação visual com histórico de mensagens fluido e ícones funcionais proporcionou uma excelente experiência de usuário (UX), mantendo as respostas do agente 'Gui' sempre rápidas, didáticas e estritamente alinhadas com as diretrizes educativas exigidas para o desafio.

**O que pode melhorar:**
- Como pontos de melhoria futura, o principal objetivo é realizar a integração completa do projeto a uma LLM de mercado. Durante o desenvolvimento, o escopo inicial foi limitado por restrições técnicas: primeiro, devido à limitação de hardware (memória RAM) do ambiente local para baixar e rodar o modelo Llama; segundo, por conta de instabilidades de rede e autenticação com chaves de APIs gratuitas de múltiplos provedores de IA (como Groq, Gemini e Cerebras), que apresentaram falhas de execução no ambiente de deploy. Para garantir a entrega e a estabilidade do app online no Streamlit Cloud, adotei uma arquitetura de contingência baseada em um motor de busca local e dicionário estático mapeado em Python, que consome as diretrizes e dados do arquivo 'produtos_financeiros.json' da pasta 'data'. Uma evolução futura natural seria estabilizar o pipeline de conexões externas via variáveis de ambiente robustas para dar capacidades generativas completas ao agente Gui.

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução, como:

- Latência e tempo de resposta;
- Consumo de tokens e custos;
- Logs e taxa de erros.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
