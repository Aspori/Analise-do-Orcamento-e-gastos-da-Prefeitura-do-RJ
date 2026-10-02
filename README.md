# 📊 Análise da Renúncia de Receita da Prefeitura do Rio de Janeiro

Projeto de análise de dados com **Python e SQL** sobre os benefícios fiscais (IPTU e ISS) que a Prefeitura do Rio concede a empresas. A ideia é responder, com dados abertos, uma pergunta simples: **quanto a cidade deixa de arrecadar, e quem recebe esse benefício?**

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-banco_local-003B57?logo=sqlite&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-análise-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/status-em_andamento-yellow)

---

## 🎯 O que o projeto faz

1. Lê a planilha oficial de renúncia de receita da Prefeitura
2. Limpa e trata os dados (cabeçalho fora do lugar, valores em texto, duplicados)
3. Grava tudo num banco **SQLite**
4. Responde perguntas com consultas **SQL**
5. Gera gráficos e conclusões a partir dos resultados

## ❓ Perguntas que a análise responde

- Quanto a Prefeitura deixou de arrecadar por ano?
- Qual tipo de renúncia pesa mais?
- Quais são as 10 empresas (CNPJ) que mais receberam benefício?
- Poucos CNPJs concentram a maior parte do valor?
- Teve crescimento ou queda ao longo dos anos?
- Existem empresas que aparecem em mais de um tipo de renúncia?

## 🗂️ Sobre os dados

| Item | Detalhe |
|---|---|
| Fonte | Portal de dados abertos da Prefeitura do Rio (Data.Rio) |
| Conjunto | Renúncia de Receita (IPTU / ISS Franquias por CNPJ) |
| Período | 01/01/2021 a 31/12/2025 |
| Formato | Planilha `.xlsx` |

**Colunas originais:**

| Coluna | O que é |
|---|---|
| ANO | Ano da renúncia |
| TIPO DE RENÚNCIA | Tipo do benefício (IPTU, ISS Franquias...) |
| CNPJ do Titular | CNPJ da empresa beneficiada |
| Nome do Titular | Nome da empresa |
| Valor Total da Renúncia | Quanto deixou de ser arrecadado (R$) |
| Quantidade de Inscrições Imobiliárias | Quantos imóveis entram no benefício |
| Inscrição | Número da inscrição imobiliária |

> As colunas de inscrição imobiliária fazem sentido para o IPTU. Nas linhas de ISS é normal ficarem vazias.

## 🧰 Tecnologias

- **Python 3.13**
- **pandas** para ler e tratar os dados
- **openpyxl** para o pandas conseguir abrir `.xlsx`
- **SQLite** para guardar os dados e rodar as consultas
- **matplotlib** para os gráficos

## 📁 Estrutura do projeto

```
.
├── data/
│   ├── data.xlsx        # planilha original da Prefeitura
│   └── data.db          # banco SQLite gerado pelo script
├── main.py              # leitura, limpeza e carga no banco
├── README.md
└── requirements.txt
```

## ▶️ Como rodar

**1. Clone o repositório**

```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
cd NOME-DO-REPOSITORIO
```

**2. Instale as dependências**

```bash
pip install pandas openpyxl matplotlib
```

**3. Coloque a planilha na pasta `data/` com o nome `data.xlsx`**

**4. Rode o script**

```bash
python main.py
```

Isso cria o arquivo `data/data.db` com a tabela `renuncia` pronta pras consultas.

## 🧹 Tratamento dos dados

A planilha original tinha alguns detalhes que precisaram de ajuste:

- **5 linhas de título** acima do cabeçalho real. Resolvido lendo com `header=5`.
- **Nomes de coluna** com espaço e acento. Renomeados para nomes simples (`ano`, `tipo_renuncia`, `cnpj`...).
- **Valores em texto** (`R$ 1.234,56`). Convertidos para número.
- **Linhas duplicadas e linhas vazias**. Removidas.

## 🔎 Consultas SQL

Alguns exemplos do que roda em cima da tabela `renuncia`:

**Total renunciado por ano**

```sql
SELECT ano, SUM(valor_total) AS total
FROM renuncia
GROUP BY ano
ORDER BY ano;
```

**Top 10 empresas com maior benefício**

```sql
SELECT nome_titular, cnpj, SUM(valor_total) AS total
FROM renuncia
GROUP BY cnpj, nome_titular
ORDER BY total DESC
LIMIT 10;
```

**Quanto os 10 maiores representam do total**

```sql
SELECT SUM(total) * 100.0 / (SELECT SUM(valor_total) FROM renuncia) AS percentual_top10
FROM (
  SELECT SUM(valor_total) AS total
  FROM renuncia
  GROUP BY cnpj
  ORDER BY total DESC
  LIMIT 10
);
```

**Empresas que aparecem em mais de um tipo de renúncia**

```sql
SELECT cnpj, nome_titular, COUNT(DISTINCT tipo_renuncia) AS tipos
FROM renuncia
GROUP BY cnpj, nome_titular
HAVING tipos > 1
ORDER BY tipos DESC;
```

## 📈 Resultados

> 🚧 **Preencher depois de rodar as análises.**

**Gráficos**

<!-- Troque pelos seus prints, por exemplo: -->
<!-- ![Renúncia por ano](imagens/renuncia_por_ano.png) -->
<!-- ![Top 10 empresas](imagens/top10.png) -->

**Principais conclusões**

1. _Descobri que..._
2. _Descobri que..._
3. _Descobri que..._

## 💡 O que eu aprendi

- Ler e tratar uma planilha real do governo, com cabeçalho fora do lugar e valores em formato brasileiro
- Modelar e consultar dados com SQL (`GROUP BY`, subconsultas, `HAVING`)
- Integrar pandas e SQLite no mesmo fluxo
- Transformar números em conclusões fáceis de explicar

## 🚀 Próximos passos

- [ ] Gerar os gráficos com matplotlib
- [ ] Escrever as conclusões da análise
- [ ] Criar um notebook Jupyter contando a história dos dados
- [ ] Comparar os tipos de renúncia ano a ano

## 👤 Autor

**Vinicius**
Estudante de Ciência da Computação (UVA), Rio de Janeiro

[GitHub](https://github.com/SEU-USUARIO) · [LinkedIn](https://linkedin.com/in/SEU-PERFIL)

---

📌 Dados públicos, usados apenas para fins de estudo.