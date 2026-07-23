# Base de Conhecimento

## Dados Utilizados



| Arquivo | Formato | Utilização no Agente |
| :--- | :--- | :--- |
| `produtos_financeiros.json` | JSON | Base de conhecimento online para comparar investimentos simulados com a Poupança e alertar sobre o CDC. |



---

## Adaptações nos Dados


Os dados simulados originais foram substituídos por uma nova estrutura em formato JSON focada em educação financeira básica. A base foi expandida para incluir taxas de mercado simuladas (como CDI a 12.00% e Selic a 12.15%) e um comparativo didático de produtos como CDB, LCI, LCA e Tesouro Selic diretamente contra o rendimento da Poupança. 


---

## Estratégia de Integração

### Como os dados são carregados?

 O JSON é carregado no início da sessão e incluído no contexto do prompt

### Como os dados são usados no prompt?

Os dados de produtos e taxas são estruturados diretamente no código fonte em um dicionário Python (JSON estruturado na memória ativa). A consulta ocorre de forma estática e local a cada interação: o motor de busca lê a pergunta do usuário e busca por palavras-chave mapeadas. Quando encontra uma correspondência (como "CDB" ou "Poupança"), o algoritmo extrai as explicações e simulações correspondentes diretamente dessa base de conhecimento interna, eliminando a dependência de requisições de rede ou injeção de prompts em LLMs externas.


---

## Exemplo de Contexto Montado


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
