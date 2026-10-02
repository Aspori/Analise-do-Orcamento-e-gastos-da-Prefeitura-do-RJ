from pathlib import Path
import sqlite3
import pandas as pd

pasta = Path(__file__).parent
con = sqlite3.connect(pasta / 'data' / 'data.db')

pd.options.display.float_format = '{:,.2f}'.format

#Perguntas a serem respondidas com consultas SQL:
'''

Quanto a Prefeitura deixou de arrecadar por ano?
Qual tipo de renúncia pesa mais?
Quais são as 10 empresas (CNPJ) que mais receberam benefício?
Poucos CNPJs concentram a maior parte do valor?
Teve crescimento ou queda ao longo dos anos?
Existem empresas que aparecem em mais de um tipo de renúncia?

'''

# função para realizar consultas no banco de dados
def consulta(sql):
    return pd.read_sql(sql, con)

# Quanto a Prefeitura deixou de arrecadar por ano? & Teve crescimento ou queda ao longo dos anos?
resultado = consulta('''
    SELECT ano, SUM(valor_total) AS total
    FROM renuncia
    GROUP BY ano
    ORDER BY ano
''')

print(resultado)
print()

# Quais são as 10 empresas (CNPJ) que mais receberam benefício?

top10 = consulta(''' 
    SELECT nome_titular, cnpj, SUM(valor_total) AS total
    FROM renuncia
    GROUP BY cnpj, nome_titular
    ORDER BY total DESC
    LIMIT 10
''')

print(top10)
print()

# Qual tipo de renúncia pesa mais? R: IPTU

tipo_pesado = consulta(''' 
    SELECT DISTINCT tipo_renuncia, SUM(valor_total) AS total
    FROM renuncia
    GROUP BY tipo_renuncia
    ORDER BY total DESC
''')

print(tipo_pesado)
print()

# Existem empresas que aparecem em mais de um tipo de renúncia?

mais_de_um_tipo = consulta(''' 
    SELECT cnpj, nome_titular, COUNT(DISTINCT tipo_renuncia) AS tipos
    FROM renuncia
    GROUP BY cnpj, nome_titular
    HAVING tipos > 1
    ORDER BY tipos DESC;
''')

print(mais_de_um_tipo)
print()

# Poucos CNPJs concentram a maior parte do valor?

# Mostra em tabela sql o percentual do top10
concentracao = consulta('''
    SELECT SUM(total) * 100.0 / (SELECT SUM(valor_total) FROM renuncia) AS percentual_top10
    FROM (
        SELECT SUM(valor_total) AS total
        FROM renuncia
        GROUP BY cnpj
        ORDER BY total DESC
        LIMIT 10
    )
''')

print(concentracao)
print()

# mostra em python Top10,20,50 o percentual do total de renúncias concentrado nos maiores CNPJs
por_cnpj = consulta('''
    SELECT cnpj, SUM(valor_total) AS total
    FROM renuncia
    GROUP BY cnpj
    ORDER BY total DESC
''')

total_geral = por_cnpj['total'].sum()

for n in [10, 20, 50]:
    soma_top = por_cnpj['total'].head(n).sum()
    print(f'Top {n}: {soma_top / total_geral * 100:.1f}% do total')

print()

# Quantidade de cnpjs

qtd_cnpj = consulta('''
    SELECT COUNT(DISTINCT cnpj) AS total_cnpjs
    FROM renuncia
''')

print(qtd_cnpj)
print()

# checagem de dados nulos e colunas tipo "total"
checagem = consulta('''
    SELECT *
    FROM renuncia
    WHERE cnpj IS NULL OR nome_titular IS NULL OR valor_total IS NULL
''')

print(checagem)
print()


con.close()
