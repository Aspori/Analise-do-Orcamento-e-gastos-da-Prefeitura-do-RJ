from pathlib import Path
import sqlite3
import pandas as pd

pasta = Path(__file__).parent
con = sqlite3.connect(pasta / 'data' / 'data.db')

pd.options.display.float_format = '{:,.2f}'.format

# função para realizar consultas no banco de dados
def consulta(sql):
    return pd.read_sql(sql, con)

# valor total de renúncias por ano (dinheiro)
resultado = consulta('''
    SELECT ano, SUM(valor_total) AS total
    FROM renuncia
    GROUP BY ano
    ORDER BY ano
''')

print(resultado)
print()
# tipos de renuncia

tipos_renuncia = consulta(''' 
    SELECT DISTINCT tipo_renuncia
    FROM renuncia
''')

print(tipos_renuncia)
print()
# top 10 empresas com maior valor de renúncia

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

# Empresas que aparecem em mais de um tipo

mais_de_um_tipo = consulta(''' 
    SELECT cnpj, nome_titular, COUNT(DISTINCT tipo_renuncia) AS tipos
    FROM renuncia
    GROUP BY cnpj, nome_titular
    HAVING tipos > 1
    ORDER BY tipos DESC;
''')

print(mais_de_um_tipo)
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
