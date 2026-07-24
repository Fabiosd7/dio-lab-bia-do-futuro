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
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 2: Recomendação de produto
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Produto compatível com o perfil do cliente
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Agente informa que só trata de finanças
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Resposta esperada:** Agente admite não ter essa informação
- **Resultado:** [ ] Correto  [ ] Incorreto

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

![Demonstração do Chat do Gui](https://githubusercontent.com)
**O que funcionou bem:**
- [Liste aqui]

**O que pode melhorar:**
- [Liste aqui]

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução, como:

- Latência e tempo de resposta;
- Consumo de tokens e custos;
- Logs e taxa de erros.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
