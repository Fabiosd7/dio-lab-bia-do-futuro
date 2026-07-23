# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:


| Arquivo | Formato | Utilização no Agente |
| :--- | :--- | :--- |
| `produtos_financeiros.json` | JSON | Base de conhecimento online para comparar investimentos simulados com a Poupança e alertar sobre o CDC. |



> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados simulados originais foram substituídos por uma nova estrutura em formato JSON focada em educação financeira básica. A base foi expandida para incluir taxas de mercado simuladas (como CDI a 12.00% e Selic a 12.15%) e um comparativo didático de produtos como CDB, LCI, LCA e Tesouro Selic diretamente contra o rendimento da Poupança. 


---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

[ex: Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt]

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados de produtos e taxas são estruturados diretamente no código fonte em um dicionário Python (JSON estruturado na memória ativa). A consulta ocorre de forma estática e local a cada interação: o motor de busca lê a pergunta do usuário e busca por palavras-chave mapeadas. Quando encontra uma correspondência (como "CDB" ou "Poupança"), o algoritmo extrai as explicações e simulações correspondentes diretamente dessa base de conhecimento interna, eliminando a dependência de requisições de rede ou injeção de prompts em LLMs externas.


---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
{
  "taxas_mercado_simuladas": {
    "CDI_ANUAL": "12.00%",
    "SELIC_ANUAL": "12.15%",
    "POUPANCA_ANUAL": "6.17%"
  },
  "produtos_bancarios": [
    {
      "sigla": "CDB",
      "nome": "Certificado de Depósito Bancário",
      "tipo": "Investimento",
      "rentabilidade_simulada": "100% do CDI (Rende aprox. 12% ao ano)",
      "comparativo_poupanca": "Rende quase o dobro da Poupança com a mesma segurança (Garantido pelo FGC)."
    }
  ]
}

...
```
